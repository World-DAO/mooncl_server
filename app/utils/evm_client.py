from web3 import Web3
from typing import Optional, Dict, Any
import json
import base64
import hashlib
from datetime import datetime
from app.config import settings


class EVMClient:
    def __init__(self):
        self._w3 = None
        self._contract = None
        self._contract_abi = None
        self._chain_id = None

    def _ensure_initialized(self):
        """确保客户端已初始化"""
        if self._w3 is None:
            self._initialize()

    def _initialize(self):
        """初始化 Web3 连接和合约"""
        self.rpc_url = settings.EVM_RPC_URL
        self.contract_address = settings.NFT_CONTRACT_ADDRESS
        self.private_key = settings.PRIVATE_KEY

        # 检查必要的配置
        if not self.rpc_url:
            raise Exception("EVM_RPC_URL 未配置，请检查 .env 文件")
        if not self.contract_address:
            raise Exception("NFT_CONTRACT_ADDRESS 未配置，请检查 .env 文件")
        if not self.private_key:
            raise Exception("PRIVATE_KEY 未配置，请检查 .env 文件")

        self._w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        # 验证连接
        if not self._w3.is_connected():
            raise Exception(f"无法连接到 Celo EVM RPC: {self.rpc_url}")

        # 获取链 ID
        self._chain_id = self._w3.eth.chain_id

        # 验证是否为 Celo 网络
        if self._chain_id not in [42220, 44787]:  # Celo 主网和 Alfajores 测试网
            print(
                f"⚠️  警告: 当前连接的网络 Chain ID ({self._chain_id}) 不是已知的 Celo 网络"
            )

        # 加载合约ABI
        try:
            with open("contracts/AiTextNFT.json", "r") as f:
                self._contract_abi = json.load(f)
        except FileNotFoundError:
            raise Exception("合约 ABI 文件 'contracts/AiTextNFT.json' 未找到")

        self._contract = self._w3.eth.contract(
            address=self.contract_address, abi=self._contract_abi
        )

    @property
    def w3(self):
        """获取 Web3 实例"""
        self._ensure_initialized()
        return self._w3

    @property
    def contract(self):
        """获取合约实例"""
        self._ensure_initialized()
        return self._contract

    @property
    def chain_id(self):
        """获取链 ID"""
        self._ensure_initialized()
        return self._chain_id

    def _generate_text_hash(self, content: str) -> bytes:
        """生成文本内容的哈希值"""
        return self.w3.keccak(text=content)

    def _generate_metadata_for_opinion(
        self, opinion_id: int, content: str, creator: str
    ) -> str:
        """为观点生成NFT元数据"""
        metadata = {
            "name": f"Opinion #{opinion_id}",
            "description": content[:200] + "..." if len(content) > 200 else content,
            "image": f"https://api.mooncl.com/api/v1/nfts/text-image/{opinion_id}",
            "attributes": [
                {"trait_type": "Opinion ID", "value": opinion_id},
                {"trait_type": "Creator", "value": creator},
                {"trait_type": "Content Length", "value": len(content)},
                {
                    "trait_type": "Text Hash",
                    "value": self._generate_text_hash(content).hex(),
                },
                {
                    "trait_type": "Created Date",
                    "value": datetime.now().strftime("%Y-%m-%d"),
                },
                {
                    "trait_type": "Network",
                    "value": "Celo",
                },
                {
                    "trait_type": "Chain ID",
                    "value": self.chain_id,
                },
            ],
            "external_url": f"https://mooncl.com/opinions/{opinion_id}",
            "content": content,
        }

        return json.dumps(metadata, ensure_ascii=False)

    def mint_nft(
        self,
        opinion_id: int,
        content: str,
        recipient_address: str,
    ) -> Dict[str, Any]:
        """在 Celo 网络上铸造NFT"""
        try:
            # 生成文本哈希
            text_hash = self._generate_text_hash(content)

            # 生成元数据URI
            metadata = self._generate_metadata_for_opinion(
                opinion_id, content, recipient_address
            )

            # 选择元数据存储方式
            metadata_uri = f"data:application/json;base64,{base64.b64encode(metadata.encode()).decode()}"

            account = self.w3.eth.account.from_key(self.private_key)

            # 检查合约铸造费用
            mint_fee = 0
            try:
                mint_fee = self.contract.functions.mintFee().call()
                if mint_fee > 0:
                    print(
                        f"💰 合约铸造费用: {mint_fee} wei ({self.w3.from_wei(mint_fee, 'ether')} CELO)"
                    )
            except Exception as fee_error:
                print(f"⚠️  无法获取铸造费用，假设为0: {fee_error}")

            # 获取当前 gas price
            gas_price = self.w3.eth.gas_price
            max_gas_price = self.w3.to_wei("10", "gwei")
            if gas_price > max_gas_price:
                gas_price = max_gas_price

            # 构建交易参数
            transaction_params = {
                "from": account.address,
                "gas": 500000,
                "gasPrice": gas_price,
                "nonce": self.w3.eth.get_transaction_count(account.address),
                "chainId": self.chain_id,
            }

            # 如果有铸造费用，添加value参数
            if mint_fee > 0:
                transaction_params["value"] = mint_fee

            # 使用合约的mintToWithContent方法
            transaction = self.contract.functions.mintToWithContent(
                recipient_address,  # to: 接收者地址
                metadata_uri,  # uri: 元数据URI
                content.encode("utf-8"),  # content: 文本内容 (bytes)
            ).build_transaction(transaction_params)

            # 签名交易
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )

            # 发送交易
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"🚀 交易已发送: {tx_hash.hex()}")

            # 等待交易确认
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            print(f"✅ 交易已确认，区块: {receipt.blockNumber}")

            # 从事件中获取token_id
            token_id = None
            for log in receipt.logs:
                try:
                    # 尝试解析Minted事件
                    decoded_log = self.contract.events.Minted().process_log(log)
                    token_id = decoded_log["args"]["tokenId"]
                    print(f"🎨 NFT铸造成功，Token ID: {token_id}")
                    break
                except:
                    # 如果没有Minted事件，尝试从Transfer事件获取
                    try:
                        decoded_log = self.contract.events.Transfer().process_log(log)
                        if (
                            decoded_log["args"]["from"]
                            == "0x0000000000000000000000000000000000000000"
                            and decoded_log["args"]["to"].lower()
                            == recipient_address.lower()
                        ):
                            token_id = decoded_log["args"]["tokenId"]
                            print(f"🎨 从Transfer事件获取Token ID: {token_id}")
                            break
                    except:
                        continue

            if token_id is None:
                print("⚠️  无法从事件中获取Token ID，但交易已成功")
                token_id = 0  # 设置默认值

            # 计算交易成本
            tx_cost_wei = receipt.gasUsed * receipt.effectiveGasPrice
            tx_cost_celo = self.w3.from_wei(tx_cost_wei, "ether")
            total_cost_wei = tx_cost_wei + mint_fee
            total_cost_celo = self.w3.from_wei(total_cost_wei, "ether")

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "token_id": token_id,
                "text_hash": text_hash.hex(),
                "gas_used": receipt.gasUsed,
                "gas_price": receipt.effectiveGasPrice,
                "mint_fee": mint_fee,
                "tx_cost_celo": float(tx_cost_celo),
                "total_cost_celo": float(total_cost_celo),
                "block_number": receipt.blockNumber,
                "network": "Celo",
                "chain_id": self.chain_id,
            }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ NFT铸造失败: {error_msg}")

            # 提供更详细的错误信息
            if "insufficient funds" in error_msg.lower():
                error_msg = f"账户余额不足，需要更多CELO代币支付Gas费用和铸造费用"
            elif "nonce too low" in error_msg.lower():
                error_msg = f"交易nonce过低，请稍后重试"
            elif "gas" in error_msg.lower():
                error_msg = f"Gas相关错误: {error_msg}"
            elif "revert" in error_msg.lower():
                error_msg = f"合约执行失败，可能是权限或参数问题: {error_msg}"

            return {"success": False, "error": error_msg}

    def get_nft_metadata(self, token_id: int) -> str:
        """获取NFT元数据URI"""
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except:
            return None

    def get_text_hash(self, token_id: int) -> str:
        """获取NFT对应的文本哈希"""
        try:
            text_hash = self.contract.functions.textHashOf(token_id).call()
            return text_hash.hex() if text_hash else None
        except:
            return None

    def get_nft_content(self, token_id: int) -> str:
        """获取NFT对应的文本内容"""
        try:
            content_bytes = self.contract.functions.contentOf(token_id).call()
            return content_bytes.decode("utf-8") if content_bytes else None
        except:
            return None

    def get_nft_price(self, token_id: int) -> int:
        """获取NFT价格"""
        try:
            return self.contract.functions.priceOf(token_id).call()
        except:
            return None

    def get_market_address(self) -> str:
        """获取当前设置的Market地址"""
        try:
            return self.contract.functions.market().call()
        except:
            return None

    def set_market_address(self, market_address: str) -> Dict[str, Any]:
        """设置Market地址 (只有合约owner可以调用)"""
        try:
            account = self.w3.eth.account.from_key(self.private_key)

            # 获取当前 gas price
            gas_price = self.w3.eth.gas_price
            max_gas_price = self.w3.to_wei("10", "gwei")
            if gas_price > max_gas_price:
                gas_price = max_gas_price

            transaction = self.contract.functions.setMarket(
                market_address
            ).build_transaction(
                {
                    "from": account.address,
                    "gas": 100000,
                    "gasPrice": gas_price,
                    "nonce": self.w3.eth.get_transaction_count(account.address),
                    "chainId": self.chain_id,
                }
            )

            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed,
                "network": "Celo",
                "chain_id": self.chain_id,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def estimate_mint_gas(self, content: str, recipient_address: str) -> Dict[str, Any]:
        """估算铸造NFT的Gas费用"""
        try:
            account = self.w3.eth.account.from_key(self.private_key)

            # 生成测试元数据
            metadata_uri = "data:application/json;base64,eyJ0ZXN0IjoidGVzdCJ9"

            # 估算Gas
            gas_estimate = self.contract.functions.mintToWithContent(
                recipient_address, metadata_uri, content.encode("utf-8")
            ).estimate_gas({"from": account.address})

            # 获取当前Gas价格
            gas_price = self.w3.eth.gas_price

            # 计算费用
            tx_cost_wei = gas_estimate * gas_price
            tx_cost_celo = self.w3.from_wei(tx_cost_wei, "ether")

            return {
                "success": True,
                "gas_estimate": gas_estimate,
                "gas_price": gas_price,
                "gas_price_gwei": self.w3.from_wei(gas_price, "gwei"),
                "tx_cost_wei": tx_cost_wei,
                "tx_cost_celo": float(tx_cost_celo),
                "network": "Celo",
                "chain_id": self.chain_id,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_network_info(self) -> Dict[str, Any]:
        """获取网络信息"""
        try:
            chain_id = self.chain_id
            latest_block = self.w3.eth.block_number
            gas_price = self.w3.eth.gas_price

            # 确定网络名称
            network_name = "Unknown"
            explorer_url = ""
            if chain_id == 42220:
                network_name = "Celo Mainnet"
                explorer_url = "https://celoscan.io"
            elif chain_id == 44787:
                network_name = "Celo Alfajores Testnet"
                explorer_url = "https://alfajores.celoscan.io"

            return {
                "success": True,
                "chain_id": chain_id,
                "network_name": network_name,
                "latest_block": latest_block,
                "gas_price": gas_price,
                "gas_price_gwei": self.w3.from_wei(gas_price, "gwei"),
                "rpc_url": self.rpc_url,
                "explorer_url": explorer_url,
                "contract_address": self.contract_address,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_connected(self) -> bool:
        """检查是否已连接"""
        try:
            return self.w3.is_connected()
        except:
            return False


# 创建单例实例（延迟初始化）
evm_client = EVMClient()

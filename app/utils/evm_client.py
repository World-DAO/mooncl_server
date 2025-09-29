from web3 import Web3
from typing import Optional, Dict, Any
import json
import base64
from datetime import datetime
from app.config import settings


class EVMClient:
    def __init__(self):
        self._w3 = None
        self._contract = None
        self._chain_id = None

    def _ensure_initialized(self):
        if self._w3 is None:
            self._initialize()

    def _initialize(self):
        try:
            self.rpc_url = settings.EVM_RPC_URL
            self.contract_address = settings.NFT_CONTRACT_ADDRESS
            self.private_key = settings.PRIVATE_KEY

            if not all([self.rpc_url, self.contract_address, self.private_key]):
                raise Exception("缺少必要配置，请检查 .env 文件")

            self._w3 = Web3(Web3.HTTPProvider(self.rpc_url))

            if self._w3.is_connected():
                self._chain_id = self._w3.eth.chain_id
            else:
                print(f"⚠️ 无法连接到 RPC: {self.rpc_url}")

            with open("contracts/AiTextNFT.json", "r") as f:
                contract_abi = json.load(f)

            self._contract = self._w3.eth.contract(
                address=self.contract_address, abi=contract_abi
            )

        except Exception as e:
            self._w3 = None
            self._contract = None
            self._chain_id = None
            raise Exception(f"初始化失败: {e}")

    @property
    def w3(self):
        self._ensure_initialized()
        return self._w3

    @property
    def contract(self):
        self._ensure_initialized()
        return self._contract

    @property
    def chain_id(self):
        self._ensure_initialized()
        return self._chain_id

    def _generate_metadata(self, opinion_id: int, content: str, creator: str) -> str:
        metadata = {
            "name": f"Opinion #{opinion_id}",
            "description": content[:200] + "..." if len(content) > 200 else content,
            "attributes": [
                {"trait_type": "Opinion ID", "value": opinion_id},
                {"trait_type": "Creator", "value": creator},
                {"trait_type": "Content Length", "value": len(content)},
                {
                    "trait_type": "Created Date",
                    "value": datetime.now().strftime("%Y-%m-%d"),
                },
                {"trait_type": "Chain ID", "value": self.chain_id},
            ],
            "content": content,
        }
        return json.dumps(metadata, ensure_ascii=False)

    def _get_gas_price(self) -> int:
        try:
            current_price = self.w3.eth.gas_price
            max_price = self.w3.to_wei("200", "gwei")
            min_price = self.w3.to_wei("50", "gwei")
            return max(min_price, min(current_price, max_price))
        except:
            return self.w3.to_wei("50", "gwei")

    def mint_nft(
        self, opinion_id: int, content: str, recipient_address: str
    ) -> Dict[str, Any]:
        try:
            self._ensure_initialized()
            account = self.w3.eth.account.from_key(self.private_key)

            # 生成元数据
            metadata = self._generate_metadata(opinion_id, content, recipient_address)
            metadata_uri = f"data:application/json;base64,{base64.b64encode(metadata.encode()).decode()}"

            # 检查铸造费用
            mint_fee = 0
            try:
                mint_fee = self.contract.functions.mintFee().call()
            except:
                pass

            # 检查余额
            balance = self.w3.eth.get_balance(account.address)
            gas_price = self._get_gas_price()
            estimated_cost = (300000 * gas_price) + mint_fee

            if balance < estimated_cost:
                return {
                    "success": False,
                    "error": f"余额不足，需要 {self.w3.from_wei(estimated_cost, 'ether')} CELO",
                }

            # 构建交易
            tx_params = {
                "from": account.address,
                "gas": 300000,
                "gasPrice": gas_price,
                "nonce": self.w3.eth.get_transaction_count(account.address),
                "chainId": self.chain_id,
            }

            if mint_fee > 0:
                tx_params["value"] = mint_fee

            encoded_content = content.encode("utf-8")

            print("encoded_content: ", encoded_content)
            print("metadata_uri: ", metadata_uri)

            transaction = self.contract.functions.mint(
                encoded_content, metadata_uri
            ).build_transaction(tx_params)

            # 签名并发送
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )

            try:
                raw_tx = signed_txn.raw_transaction
            except AttributeError:
                raw_tx = signed_txn.rawTransaction

            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if receipt.status == 0:
                return {
                    "success": False,
                    "error": "交易执行失败",
                    "transaction_hash": tx_hash.hex(),
                }

            # 提取 token_id
            token_id = None
            for log in receipt.logs:
                try:
                    decoded_log = self.contract.events.Transfer().process_log(log)
                    if (
                        decoded_log["args"]["from"]
                        == "0x0000000000000000000000000000000000000000"
                    ):
                        token_id = decoded_log["args"]["tokenId"]
                        break
                except:
                    continue

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "token_id": token_id,
                "gas_used": receipt.gasUsed,
                "total_cost_celo": float(
                    self.w3.from_wei(receipt.gasUsed * gas_price + mint_fee, "ether")
                ),
                "chain_id": self.chain_id,
            }

        except Exception as e:
            error_msg = str(e)
            if "insufficient funds" in error_msg.lower():
                return {"success": False, "error": "账户余额不足"}
            elif "nonce too low" in error_msg.lower():
                return {"success": False, "error": "交易nonce过低，请重试"}
            else:
                return {"success": False, "error": f"铸造失败: {error_msg}"}

    def get_nft_metadata(self, token_id: int) -> str:
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except:
            return None

    def get_text_hash(self, token_id: int) -> str:
        try:
            text_hash = self.contract.functions.textHashOf(token_id).call()
            return text_hash.hex() if text_hash else None
        except:
            return None

    def get_nft_content(self, token_id: int) -> str:
        try:
            content_bytes = self.contract.functions.contentOf(token_id).call()
            return content_bytes.decode("utf-8") if content_bytes else None
        except:
            return None

    def get_market_address(self) -> str:
        try:
            return self.contract.functions.market().call()
        except:
            return None

    def set_market_address(self, market_address: str) -> Dict[str, Any]:
        try:
            account = self.w3.eth.account.from_key(self.private_key)
            gas_price = self._get_gas_price()

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

            try:
                raw_tx = signed_txn.raw_transaction
            except AttributeError:
                raw_tx = signed_txn.rawTransaction

            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_network_info(self) -> Dict[str, Any]:
        try:
            chain_id = self.chain_id
            network_name = (
                "Celo Mainnet"
                if chain_id == 42220
                else "Celo Alfajores" if chain_id == 44787 else "Unknown"
            )

            return {
                "success": True,
                "chain_id": chain_id,
                "network_name": network_name,
                "latest_block": self.w3.eth.block_number,
                "gas_price_gwei": float(
                    self.w3.from_wei(self.w3.eth.gas_price, "gwei")
                ),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_connected(self) -> bool:
        try:
            self._ensure_initialized()
            return self._w3 is not None and self._w3.is_connected()
        except:
            return False

    def set_nft_price(self, token_id: int, price_wei: int) -> Dict[str, Any]:
        """设置NFT价格"""
        try:
            self._ensure_initialized()
            account = self.w3.eth.account.from_key(self.private_key)

            # 检查余额
            balance = self.w3.eth.get_balance(account.address)
            gas_price = self._get_gas_price()
            estimated_cost = 100000 * gas_price  # 估算gas费用

            if balance < estimated_cost:
                return {
                    "success": False,
                    "error": f"余额不足，需要 {self.w3.from_wei(estimated_cost, 'ether')} CELO",
                }

            # 构建交易
            transaction = self.contract.functions.setPrice(
                token_id, price_wei
            ).build_transaction(
                {
                    "from": account.address,
                    "gas": 100000,
                    "gasPrice": gas_price,
                    "nonce": self.w3.eth.get_transaction_count(account.address),
                    "chainId": self.chain_id,
                }
            )

            # 签名并发送交易
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )

            try:
                raw_tx = signed_txn.raw_transaction
            except AttributeError:
                raw_tx = signed_txn.rawTransaction

            tx_hash = self.w3.eth.send_raw_transaction(raw_tx)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed,
                "token_id": token_id,
                "price_wei": price_wei,
                "price_eth": float(self.w3.from_wei(price_wei, "ether")),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


# 创建全局实例
evm_client = EVMClient()

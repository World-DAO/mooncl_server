from web3 import Web3
from typing import Optional, Dict, Any
import json
from app.config import settings


class EVMClient:
    def __init__(self):
        self.rpc_url = settings.EVM_RPC_URL
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract_address = settings.NFT_CONTRACT_ADDRESS
        self.private_key = settings.PRIVATE_KEY

        # 加载合约ABI
        with open("contracts/NFT_ABI.json", "r") as f:
            self.contract_abi = json.load(f)

        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.contract_abi
        )

    def mint_nft(
        self,
        opinion_id: int,
        content: str,
        recipient_address: str,
    ) -> Dict[str, Any]:
        """铸造NFT"""
        try:
            # 构建交易
            account = self.w3.eth.account.from_key(self.private_key)

            # 构建交易
            transaction = self.contract.functions.mintNFT(
                recipient_address, opinion_id, metadata_uri
            ).build_transaction(
                {
                    "from": account.address,
                    "gas": 500000,
                    "gasPrice": self.w3.to_wei("20", "gwei"),
                    "nonce": self.w3.eth.get_transaction_count(account.address),
                }
            )

            # 签名交易
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )

            # 发送交易
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            # 等待交易确认
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            # 从事件中获取token_id
            token_id = None
            for log in receipt.logs:
                try:
                    decoded_log = self.contract.events.Transfer().process_log(log)
                    if decoded_log["args"]["to"].lower() == recipient_address.lower():
                        token_id = decoded_log["args"]["tokenId"]
                        break
                except:
                    continue

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "token_id": token_id,
                "gas_used": receipt.gasUsed,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def transfer_nft(
        self, token_id: int, from_address: str, to_address: str
    ) -> Dict[str, Any]:
        """转移NFT"""
        try:
            account = self.w3.eth.account.from_key(self.private_key)

            transaction = self.contract.functions.transferFrom(
                from_address, to_address, token_id
            ).build_transaction(
                {
                    "from": account.address,
                    "gas": 200000,
                    "gasPrice": self.w3.to_wei("20", "gwei"),
                    "nonce": self.w3.eth.get_transaction_count(account.address),
                }
            )

            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, self.private_key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "gas_used": receipt.gasUsed,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_nft_owner(self, token_id: int) -> str:
        """获取NFT所有者"""
        try:
            return self.contract.functions.ownerOf(token_id).call()
        except:
            return None

    def get_nft_metadata(self, token_id: int) -> str:
        """获取NFT元数据URI"""
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except:
            return None


# 单例实例
evm_client = EVMClient()

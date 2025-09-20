from sqlalchemy.orm import Session
from app.dao.nft_dao import NFTDAO
from app.dao.opinion_dao import OpinionDAO
from app.services.opinion_service import OpinionService
from app.models import (
    MintNFTResponse,
    TransferNFTResponse,
    NFTListResponse,
    MintEstimateResponse,
    PurchaseEstimateResponse,
    PurchaseNFTResponse,
)
from datetime import datetime
from typing import List
import uuid
from app.utils.sui_client import sui_client
import asyncio
from app.utils.evm_client import evm_client


class NFTService:
    @staticmethod
    def mint_nft(db: Session, opinion_id: int, creator: str) -> MintNFTResponse:
        """将观点铸造为NFT"""
        # 获取观点信息
        opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not opinion:
            return MintNFTResponse(success=False, error="Opinion not found")

        # 检查观点是否已经铸造为NFT
        if opinion.is_minted:
            return MintNFTResponse(success=False, error="Opinion already minted as NFT")

        # 检查创建者是否是观点作者
        if opinion.address != creator:
            return MintNFTResponse(
                success=False, error="Only the author can mint this opinion"
            )

        try:

            # 调用EVM合约铸造NFT
            result = evm_client.mint_nft(
                opinion_id=opinion_id,
                content=opinion.content,
                recipient_address=creator,
            )

            if not result["success"]:
                return MintNFTResponse(
                    success=False,
                    error=f"Blockchain transaction failed: {result['error']}",
                )

            # 创建数据库NFT记录
            nft_data = {
                "token_id": str(result["token_id"]),
                "opinion_id": opinion_id,
                "owner_address": creator,
                "mint_price": float(opinion.evaluate_price),
                "current_price": None,
                "is_for_sale": False,
            }

            # 保存NFT记录到数据库
            db_nft = NFTDAO.create(db, nft_data)

            # 更新观点状态为已铸造
            OpinionService.mark_as_minted(db, opinion_id)

            # 返回铸造结果
            return MintNFTResponse(
                success=True,
                nft_id=db_nft.id,
                token_id=str(result["token_id"]),
                transaction_hash=result["transaction_hash"],
            )

        except Exception as e:
            return MintNFTResponse(success=False, error=f"Failed to mint NFT: {str(e)}")

    @staticmethod
    def transfer_nft(
        db: Session, nft_id: int, from_address: str, to_address: str
    ) -> TransferNFTResponse:
        """转移NFT所有权"""
        # 获取NFT信息
        nft = NFTDAO.get_by_id(db, nft_id)
        if not nft:
            return TransferNFTResponse(success=False, error="NFT not found")

        # 检查转出者是否是当前所有者
        if nft.owner_address.lower() != from_address.lower():
            return TransferNFTResponse(
                success=False, error="Only the owner can transfer this NFT"
            )

        try:
            # 调用EVM合约转移NFT
            result = evm_client.transfer_nft(
                token_id=int(nft.token_id),
                from_address=from_address,
                to_address=to_address,
            )

            if not result["success"]:
                return TransferNFTResponse(
                    success=False,
                    error=f"Blockchain transaction failed: {result['error']}",
                )

            # 更新数据库中的所有者信息
            NFTDAO.update_owner(db, nft_id, to_address)

            return TransferNFTResponse(
                success=True,
                nft_id=nft_id,
                from_address=from_address,
                to_address=to_address,
                transaction_hash=result["transaction_hash"],
            )

        except Exception as e:
            return TransferNFTResponse(
                success=False, error=f"Failed to transfer NFT: {str(e)}"
            )

    @staticmethod
    def get_user_nfts(db: Session, owner: str) -> List[NFTListResponse]:
        """获取用户拥有的NFT列表"""
        nfts = NFTDAO.get_by_owner(db, owner)
        return [
            NFTListResponse(
                id=nft.id,
                token_id=nft.token_id,
                owner=nft.owner,
                creator=nft.creator,
                created_at=nft.created_at,
                opinion_content=nft.opinion.content if nft.opinion else "",
                opinion_title=f"Opinion #{nft.opinion_id}" if nft.opinion else "",
            )
            for nft in nfts
        ]

    @staticmethod
    def get_mint_estimate(db: Session, opinion_id: int) -> MintEstimateResponse:
        """获取NFT铸造估价"""
        # 获取观点信息
        opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not opinion:
            return MintEstimateResponse(success=False, error="Opinion not found")

        # 检查观点是否已经铸造为NFT
        if opinion.is_minted:
            return MintEstimateResponse(
                success=False, error="Opinion already minted as NFT"
            )

        # 计算铸造费用
        base_fee = 0.005  # 基础铸造费用 ETH
        content_fee = len(opinion.content) * 0.0001  # 内容长度费用
        popularity_fee = opinion.likes * 0.0005  # 受欢迎程度费用

        total_fee = base_fee + content_fee + popularity_fee

        return MintEstimateResponse(
            success=True,
            opinion_id=opinion_id,
            estimated_fee=round(total_fee, 6),
            currency="ETH",
        )

    @staticmethod
    def get_purchase_estimate(db: Session, nft_id: int) -> PurchaseEstimateResponse:
        """获取NFT购买估价"""
        # 获取NFT信息
        nft = NFTDAO.get_by_id(db, nft_id)
        if not nft:
            return PurchaseEstimateResponse(success=False, error="NFT not found")

        # 计算购买价格
        base_price = 0.01

        if nft.opinion:
            like_bonus = nft.opinion.likes * 0.002
            days_old = (datetime.utcnow() - nft.created_at).days
            time_factor = max(0.8, 1 - (days_old * 0.005))
        else:
            like_bonus = 0
            time_factor = 1

        # 交易历史影响价格
        transaction_count = (
            len(nft.transaction_history) if nft.transaction_history else 1
        )
        transaction_factor = 1 + (transaction_count - 1) * 0.1  # 每次交易增加10%价值

        estimated_price = (base_price + like_bonus) * time_factor * transaction_factor

        return PurchaseEstimateResponse(
            success=True,
            nft_id=nft_id,
            estimated_price=round(estimated_price, 6),
            currency="ETH",
        )

    @staticmethod
    def purchase_nft(
        db: Session, nft_id: int, buyer: str, price: float
    ) -> PurchaseNFTResponse:
        """购买NFT"""
        # 获取NFT信息
        nft = NFTDAO.get_by_id(db, nft_id)
        if not nft:
            return PurchaseNFTResponse(success=False, error="NFT not found")

        # 检查买家不能是当前所有者
        if nft.owner == buyer:
            return PurchaseNFTResponse(
                success=False, error="Cannot purchase your own NFT"
            )

        # 获取估价进行价格验证
        estimate = NFTService.get_purchase_estimate(db, nft_id)
        if not estimate.success:
            return PurchaseNFTResponse(
                success=False, error="Failed to get price estimate"
            )

        if price < estimate.estimated_price * 0.9:
            return PurchaseNFTResponse(
                success=False,
                error=f"Price too low. Minimum price: {estimate.estimated_price * 0.9:.6f} ETH",
            )

        # 创建购买交易记录
        transaction_data = {
            "type": "purchase",
            "from": nft.owner,
            "to": buyer,
            "price": price,
            "currency": "ETH",
            "timestamp": datetime.utcnow().isoformat(),
            "transaction_hash": f"tx-{uuid.uuid4()}",
        }

        # 更新NFT所有者
        success = NFTDAO.update_owner(db, nft_id, buyer, transaction_data)

        if not success:
            return PurchaseNFTResponse(
                success=False, error="Failed to update NFT ownership"
            )

        return PurchaseNFTResponse(
            success=True,
            nft_id=nft_id,
            buyer=buyer,
            seller=nft.owner,
            price=price,
            currency="ETH",
            transaction_hash=transaction_data["transaction_hash"],
        )

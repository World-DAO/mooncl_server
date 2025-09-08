from sqlalchemy.orm import Session
from app.dao.opinion_dao import OpinionDAO
from app.models import OpinionResponse, OpinionRankingResponse, OpinionPriceResponse
from datetime import datetime
from typing import Optional, List


class OpinionService:
    @staticmethod
    def create_opinion(db: Session, content: str, address: str) -> OpinionResponse:
        """创建新观点"""
        opinion_data = {
            "content": content,
            "address": address,
            "likes": 0,
            "is_minted": False,
        }

        db_opinion = OpinionDAO.create(db, opinion_data)

        return OpinionResponse(
            id=db_opinion.id,
            content=db_opinion.content,
            address=db_opinion.address,
            created_at=db_opinion.created_at,
            likes=db_opinion.likes,
            is_minted=db_opinion.is_minted,
            nft_id=db_opinion.nft_id,
        )

    @staticmethod
    def get_opinion(db: Session, opinion_id: int) -> Optional[OpinionResponse]:
        """获取观点详情"""
        db_opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not db_opinion:
            return None

        return OpinionResponse(
            id=db_opinion.id,
            content=db_opinion.content,
            address=db_opinion.address,
            created_at=db_opinion.created_at,
            likes=db_opinion.likes,
            is_minted=db_opinion.is_minted,
            nft_id=db_opinion.nft_id,
        )

    @staticmethod
    def get_opinions_by_address(db: Session, address: str) -> List[OpinionResponse]:
        """获取用户的所有观点"""
        db_opinions = OpinionDAO.get_by_address(db, address)
        return [
            OpinionResponse(
                id=opinion.id,
                content=opinion.content,
                address=opinion.address,
                created_at=opinion.created_at,
                likes=opinion.likes,
                is_minted=opinion.is_minted,
                nft_id=opinion.nft_id,
            )
            for opinion in db_opinions
        ]

    @staticmethod
    def get_opinion_ranking(
        db: Session, limit: int = 10
    ) -> List[OpinionRankingResponse]:
        """获取观点排行榜"""
        db_opinions = OpinionDAO.get_ranking(db, limit)
        return [
            OpinionRankingResponse(
                id=opinion.id,
                content=opinion.content,
                address=opinion.address,
                likes=opinion.likes,
                rank=idx + 1,
            )
            for idx, opinion in enumerate(db_opinions)
        ]

    @staticmethod
    def get_opinion_price(
        db: Session, opinion_id: int
    ) -> Optional[OpinionPriceResponse]:
        """获取观点价格"""
        db_opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not db_opinion:
            return None

        base_price = 0.01
        like_bonus = db_opinion.likes * 0.001
        days_old = (datetime.utcnow() - db_opinion.created_at).days
        time_factor = max(0.5, 1 - (days_old * 0.01))

        final_price = (base_price + like_bonus) * time_factor

        return OpinionPriceResponse(
            opinion_id=opinion_id, price=round(final_price, 6), currency="ETH"
        )

    @staticmethod
    def mark_as_minted(db: Session, opinion_id: int, nft_id: int) -> bool:
        """将观点标记为已铸造NFT"""
        return OpinionDAO.update(
            db,
            opinion_id,
            {"is_minted": True, "nft_id": nft_id, "updated_at": datetime.utcnow()},
        )

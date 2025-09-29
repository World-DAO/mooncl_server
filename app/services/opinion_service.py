from sqlalchemy.orm import Session
from app.dao.opinion_dao import OpinionDAO
from app.models import OpinionResponse, OpinionPriceResponse
from app.utils.evaluate_opinion import calculate_opinion_price
from datetime import datetime
from typing import Optional, List


class OpinionService:
    @staticmethod
    def create_opinion(db: Session, content: str, address: str) -> OpinionResponse:
        """创建新观点"""
        opinion_data = {
            "content": content,
            "address": address,
            "is_minted": False,
            "evaluate_price": 0.0,
        }

        db_opinion = OpinionDAO.create(db, opinion_data)
        OpinionService.evaluate_opinion_price(db, db_opinion.id)

        return OpinionResponse(
            id=db_opinion.id,
            address=db_opinion.address,
            content=db_opinion.content,
            is_minted=db_opinion.is_minted,
            evaluate_price=float(db_opinion.evaluate_price),
            created_at=db_opinion.created_at,
            updated_at=db_opinion.updated_at,
        )

    @staticmethod
    def get_opinion(db: Session, opinion_id: int) -> Optional[OpinionResponse]:
        """获取观点详情"""
        db_opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not db_opinion:
            return None

        return OpinionResponse(
            id=db_opinion.id,
            address=db_opinion.address,
            content=db_opinion.content,
            is_minted=db_opinion.is_minted,
            evaluate_price=float(db_opinion.evaluate_price),
            created_at=db_opinion.created_at,
            updated_at=db_opinion.updated_at,
        )

    @staticmethod
    def get_opinions_by_address(db: Session, address: str) -> List[OpinionResponse]:
        """获取用户的所有观点"""
        db_opinions = OpinionDAO.get_by_address(db, address)
        return [
            OpinionResponse(
                id=opinion.id,
                address=opinion.address,
                content=opinion.content,
                is_minted=opinion.is_minted,
                evaluate_price=float(opinion.evaluate_price),
                created_at=opinion.created_at,
                updated_at=opinion.updated_at,
            )
            for opinion in db_opinions
        ]

    @staticmethod
    def get_opinion_ranking(
        db: Session, sort_by: str = "price", limit: int = 10, offset: int = 0
    ) -> List[OpinionResponse]:
        """获取观点排行榜"""
        db_opinions = OpinionDAO.get_ranking(db, sort_by, limit, offset)
        return [
            OpinionResponse(
                id=opinion.id,
                address=opinion.address,
                content=opinion.content,
                is_minted=opinion.is_minted,
                evaluate_price=float(opinion.evaluate_price),
                created_at=opinion.created_at,
                updated_at=opinion.updated_at,
            )
            for opinion in db_opinions
        ]

    @staticmethod
    def evaluate_opinion_price(
        db: Session, opinion_id: int
    ) -> Optional[OpinionPriceResponse]:
        """评估观点价格"""
        db_opinion = OpinionDAO.get_by_id(db, opinion_id)
        if not db_opinion:
            return None

        final_price = calculate_opinion_price(db_opinion.content, db_opinion.created_at)

        # 更新数据库中的评估价格
        OpinionDAO.update_evaluate_price(db, opinion_id, final_price)

        return OpinionPriceResponse(
            opinion_id=opinion_id, price=final_price, currency="ETH"
        )

    @staticmethod
    def mark_as_minted(db: Session, opinion_id: int) -> bool:
        """将观点标记为已铸造NFT"""
        return OpinionDAO.update_mint_status(db, opinion_id, True)

    @staticmethod
    def get_unminted_opinions(db: Session, limit: int = 100) -> List[OpinionResponse]:
        """获取未铸造的观点"""
        db_opinions = OpinionDAO.get_unminted(db, limit)
        return [
            OpinionResponse(
                id=opinion.id,
                address=opinion.address,
                content=opinion.content,
                is_minted=opinion.is_minted,
                evaluate_price=float(opinion.evaluate_price),
                created_at=opinion.created_at,
                updated_at=opinion.updated_at,
            )
            for opinion in db_opinions
        ]

    @staticmethod
    def get_minted_opinions(db: Session, limit: int = 100) -> List[OpinionResponse]:
        """获取已铸造的观点"""
        db_opinions = OpinionDAO.get_minted(db, limit)
        return [
            OpinionResponse(
                id=opinion.id,
                address=opinion.address,
                content=opinion.content,
                is_minted=opinion.is_minted,
                evaluate_price=float(opinion.evaluate_price),
                created_at=opinion.created_at,
                updated_at=opinion.updated_at,
            )
            for opinion in db_opinions
        ]

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.models import NFTDB, OpinionDB
from typing import List, Optional, Dict, Any


class NFTDAO:
    @staticmethod
    def create(db: Session, nft_data: Dict[str, Any]) -> NFTDB:
        """创建新NFT"""
        db_nft = NFTDB(**nft_data)
        db.add(db_nft)
        db.commit()
        db.refresh(db_nft)
        return db_nft

    @staticmethod
    def get_by_id(db: Session, nft_id: int) -> Optional[NFTDB]:
        """根据ID获取NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.id == nft_id)
            .first()
        )

    @staticmethod
    def get_by_token_id(db: Session, token_id: str) -> Optional[NFTDB]:
        """根据链上Token ID获取NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.token_id == token_id)
            .first()
        )

    @staticmethod
    def get_by_owner_address(
        db: Session, owner_address: str, limit: int = 100
    ) -> List[NFTDB]:
        """获取用户拥有的所有NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.owner_address == owner_address)
            .order_by(desc(NFTDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_opinion_id(db: Session, opinion_id: int) -> Optional[NFTDB]:
        """根据观点ID获取NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.opinion_id == opinion_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[NFTDB]:
        """获取所有NFT（分页）"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .order_by(desc(NFTDB.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_for_sale(db: Session, skip: int = 0, limit: int = 100) -> List[NFTDB]:
        """获取在售的NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.is_for_sale == True)
            .order_by(desc(NFTDB.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_owner(db: Session, nft_id: int, new_owner_address: str) -> bool:
        """更新NFT所有者"""
        result = (
            db.query(NFTDB)
            .filter(NFTDB.id == nft_id)
            .update({"owner_address": new_owner_address})
        )
        db.commit()
        return result > 0

    @staticmethod
    def update_price(db: Session, nft_id: int, current_price: float) -> bool:
        """更新NFT当前价格"""
        result = (
            db.query(NFTDB)
            .filter(NFTDB.id == nft_id)
            .update({"current_price": current_price})
        )
        db.commit()
        return result > 0

    @staticmethod
    def update_sale_status(
        db: Session,
        nft_id: int,
        is_for_sale: bool,
        current_price: Optional[float] = None,
    ) -> bool:
        """更新NFT销售状态"""
        update_data = {"is_for_sale": is_for_sale}
        if current_price is not None:
            update_data["current_price"] = current_price

        result = db.query(NFTDB).filter(NFTDB.id == nft_id).update(update_data)
        db.commit()
        return result > 0

    @staticmethod
    def update(db: Session, nft_id: int, update_data: Dict[str, Any]) -> bool:
        """更新NFT信息"""
        result = db.query(NFTDB).filter(NFTDB.id == nft_id).update(update_data)
        db.commit()
        return result > 0

    @staticmethod
    def delete(db: Session, nft_id: int) -> bool:
        """删除NFT"""
        result = db.query(NFTDB).filter(NFTDB.id == nft_id).delete()
        db.commit()
        return result > 0

    @staticmethod
    def count_all(db: Session) -> int:
        """获取NFT总数"""
        return db.query(NFTDB).count()

    @staticmethod
    def count_by_owner(db: Session, owner_address: str) -> int:
        """获取用户拥有的NFT数量"""
        return db.query(NFTDB).filter(NFTDB.owner_address == owner_address).count()

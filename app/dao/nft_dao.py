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
    def get_by_owner(db: Session, owner: str, limit: int = 100) -> List[NFTDB]:
        """获取用户拥有的所有NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.owner == owner)
            .order_by(desc(NFTDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_creator(db: Session, creator: str, limit: int = 100) -> List[NFTDB]:
        """获取用户创建的所有NFT"""
        return (
            db.query(NFTDB)
            .options(joinedload(NFTDB.opinion))
            .filter(NFTDB.creator == creator)
            .order_by(desc(NFTDB.created_at))
            .limit(limit)
            .all()
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
    def update_owner(
        db: Session, nft_id: int, new_owner: str, transaction_data: Dict[str, Any]
    ) -> bool:
        """更新NFT所有者并添加交易记录"""
        nft = db.query(NFTDB).filter(NFTDB.id == nft_id).first()
        if nft:
            nft.owner = new_owner
            if nft.transaction_history is None:
                nft.transaction_history = []
            nft.transaction_history.append(transaction_data)
            db.commit()
            return True
        return False

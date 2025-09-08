from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import OpinionDB
from typing import List, Optional, Dict, Any


class OpinionDAO:
    @staticmethod
    def create(db: Session, opinion_data: Dict[str, Any]) -> OpinionDB:
        """创建新观点"""
        db_opinion = OpinionDB(**opinion_data)
        db.add(db_opinion)
        db.commit()
        db.refresh(db_opinion)
        return db_opinion

    @staticmethod
    def get_by_id(db: Session, opinion_id: int) -> Optional[OpinionDB]:
        """根据ID获取观点"""
        return db.query(OpinionDB).filter(OpinionDB.id == opinion_id).first()

    @staticmethod
    def get_by_address(db: Session, address: str, limit: int = 100) -> List[OpinionDB]:
        """获取用户的所有观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.address == address)
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[OpinionDB]:
        """获取所有观点（分页）"""
        return (
            db.query(OpinionDB)
            .order_by(desc(OpinionDB.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(db: Session, opinion_id: int, update_data: Dict[str, Any]) -> bool:
        """更新观点"""
        result = (
            db.query(OpinionDB).filter(OpinionDB.id == opinion_id).update(update_data)
        )
        db.commit()
        return result > 0

    @staticmethod
    def delete(db: Session, opinion_id: int) -> bool:
        """删除观点"""
        result = db.query(OpinionDB).filter(OpinionDB.id == opinion_id).delete()
        db.commit()
        return result > 0

    @staticmethod
    def get_ranking(
        db: Session, sort_by: str, limit: int, offset: int
    ) -> List[OpinionDB]:
        """获取观点排行榜"""
        query = db.query(OpinionDB)

        if sort_by == "likes":
            query = query.order_by(desc(OpinionDB.likes))
        elif sort_by == "latest":
            query = query.order_by(desc(OpinionDB.created_at))
        elif sort_by == "comments":
            query = query.order_by(desc(OpinionDB.likes))
        else:
            query = query.order_by(desc(OpinionDB.likes), desc(OpinionDB.created_at))

        return query.offset(offset).limit(limit).all()

    @staticmethod
    def count_all(db: Session) -> int:
        """获取观点总数"""
        return db.query(OpinionDB).count()

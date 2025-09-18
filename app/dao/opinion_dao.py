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
        """通过用户地址获取观点列表"""
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

        if sort_by == "latest":
            query = query.order_by(desc(OpinionDB.created_at))
        elif sort_by == "price":
            query = query.order_by(desc(OpinionDB.evaluate_price))
        else:
            # 默认按创建时间排序
            query = query.order_by(desc(OpinionDB.created_at))

        return query.offset(offset).limit(limit).all()

    @staticmethod
    def count_all(db: Session) -> int:
        """获取观点总数"""
        return db.query(OpinionDB).count()

    @staticmethod
    def count_by_address(db: Session, address: str) -> int:
        """获取指定地址的观点总数"""
        return db.query(OpinionDB).filter(OpinionDB.address == address).count()

    @staticmethod
    def get_unminted(db: Session, limit: int = 100) -> List[OpinionDB]:
        """获取未铸造的观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.is_minted == False)
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_minted(db: Session, limit: int = 100) -> List[OpinionDB]:
        """获取已铸造的观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.is_minted == True)
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_unminted_by_address(
        db: Session, address: str, limit: int = 100
    ) -> List[OpinionDB]:
        """获取指定地址的未铸造观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.address == address, OpinionDB.is_minted == False)
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_minted_by_address(
        db: Session, address: str, limit: int = 100
    ) -> List[OpinionDB]:
        """获取指定地址的已铸造观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.address == address, OpinionDB.is_minted == True)
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_mint_status(
        db: Session, opinion_id: int, is_minted: bool = True
    ) -> bool:
        """更新观点的铸造状态"""
        result = (
            db.query(OpinionDB)
            .filter(OpinionDB.id == opinion_id)
            .update({"is_minted": is_minted})
        )
        db.commit()
        return result > 0

    @staticmethod
    def update_evaluate_price(db: Session, opinion_id: int, price: float) -> bool:
        """更新观点的评估价格"""
        result = (
            db.query(OpinionDB)
            .filter(OpinionDB.id == opinion_id)
            .update({"evaluate_price": price})
        )
        db.commit()
        return result > 0

    @staticmethod
    def get_top_valued(db: Session, limit: int = 10) -> List[OpinionDB]:
        """获取评估价格最高的观点"""
        return (
            db.query(OpinionDB)
            .order_by(desc(OpinionDB.evaluate_price))
            .limit(limit)
            .all()
        )

    @staticmethod
    def search_by_content(
        db: Session, keyword: str, limit: int = 100
    ) -> List[OpinionDB]:
        """根据内容关键词搜索观点"""
        return (
            db.query(OpinionDB)
            .filter(OpinionDB.content.contains(keyword))
            .order_by(desc(OpinionDB.created_at))
            .limit(limit)
            .all()
        )

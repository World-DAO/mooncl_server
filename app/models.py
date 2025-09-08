from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.database import Base


# SQLAlchemy ORM 模型
class OpinionDB(Base):
    __tablename__ = "opinions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(Text, nullable=False)
    address = Column(String(255), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    likes = Column(Integer, default=0)
    is_minted = Column(Boolean, default=False)
    nft_id = Column(Integer, ForeignKey("nfts.id"), nullable=True)

    # 关系
    nft = relationship("NFTDB", back_populates="opinion")


class NFTDB(Base):
    __tablename__ = "nfts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    opinion_id = Column(Integer, ForeignKey("opinions.id"), nullable=False)
    owner = Column(String(255), nullable=False, index=True)
    creator = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    transaction_history = Column(JSON)  # MySQL支持JSON类型
    metadata = Column(JSON)  # 存储NFT元数据

    # 关系
    opinion = relationship("OpinionDB", back_populates="nft")


# Pydantic 模型（API请求和响应）
class OpinionCreate(BaseModel):
    content: str


class OpinionResponse(BaseModel):
    id: int
    content: str
    address: str
    created_at: datetime
    likes: int
    is_minted: bool
    nft_id: Optional[int] = None

    class Config:
        from_attributes = True


class MintNFTRequest(BaseModel):
    opinion_id: int


class MintNFTResponse(BaseModel):
    success: bool
    nft_id: Optional[int] = None
    token_id: Optional[str] = None
    transaction_hash: Optional[str] = None
    error: Optional[str] = None


class TransferNFTRequest(BaseModel):
    nft_id: int
    to_address: str


class TransferNFTResponse(BaseModel):
    success: bool
    nft_id: Optional[int] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    transaction_hash: Optional[str] = None
    error: Optional[str] = None


class NFTListResponse(BaseModel):
    id: int
    token_id: str
    owner: str
    creator: str
    created_at: datetime
    opinion_title: str
    opinion_content: str

    class Config:
        from_attributes = True


class PurchaseNFTRequest(BaseModel):
    nft_id: int


class PurchaseNFTResponse(BaseModel):
    success: bool
    nft_id: Optional[int] = None
    buyer_address: Optional[str] = None
    seller_address: Optional[str] = None
    sale_price: Optional[float] = None
    transaction_hash: Optional[str] = None
    error: Optional[str] = None

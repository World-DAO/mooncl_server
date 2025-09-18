from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    JSON,
    DECIMAL,
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
    address = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_minted = Column(Boolean, default=False)
    evaluate_price = Column(DECIMAL(20, 8), default=0.00000000)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # 关系
    nft = relationship("NFTDB", back_populates="opinion", uselist=False)


class NFTDB(Base):
    __tablename__ = "nft"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    opinion_id = Column(Integer, ForeignKey("opinions.id"), nullable=False, index=True)
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    owner_address = Column(String(255), nullable=False, index=True)
    mint_price = Column(DECIMAL(20, 8), nullable=False)
    current_price = Column(DECIMAL(20, 8), nullable=True)
    is_for_sale = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # 关系
    opinion = relationship("OpinionDB", back_populates="nft")


# Pydantic 模型（API请求和响应）
class OpinionCreate(BaseModel):
    content: str


class OpinionResponse(BaseModel):
    id: int
    address: str
    content: str
    is_minted: bool
    evaluate_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OpinionPriceResponse(BaseModel):
    opinion_id: int
    price: float
    currency: str = "ETH"


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


class NFTResponse(BaseModel):
    id: int
    opinion_id: int
    token_id: str
    owner_address: str
    mint_price: float
    current_price: Optional[float] = None
    is_for_sale: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NFTListResponse(BaseModel):
    id: int
    token_id: str
    owner_address: str
    mint_price: float
    current_price: Optional[float] = None
    is_for_sale: bool
    created_at: datetime
    opinion_content: str

    class Config:
        from_attributes = True


class PurchaseNFTRequest(BaseModel):
    nft_id: int


class PurchaseNFTResponse(BaseModel):
    success: bool
    nft_id: Optional[int] = None
    buyer: Optional[str] = None
    seller: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    transaction_hash: Optional[str] = None
    error: Optional[str] = None


class MintEstimateResponse(BaseModel):
    success: bool
    opinion_id: Optional[int] = None
    estimated_fee: Optional[float] = None
    currency: Optional[str] = "ETH"
    error: Optional[str] = None


class PurchaseEstimateResponse(BaseModel):
    success: bool
    nft_id: Optional[int] = None
    estimated_price: Optional[float] = None
    currency: Optional[str] = "ETH"
    error: Optional[str] = None

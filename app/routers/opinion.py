from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.models import OpinionCreate, OpinionResponse
from app.services.opinion_service import OpinionService
from app.utils.jwt_auth import authenticate
from app.database import get_db
from typing import List


router = APIRouter()


@router.post("/", response_model=OpinionResponse)
def create_opinion(
    request: OpinionCreate,
    address: str = Depends(authenticate),
    db: Session = Depends(get_db),
):
    """创建新观点"""
    try:
        return OpinionService.create_opinion(db, request.content, address)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create opinion: {str(e)}",
        )


@router.get("/ranking")
def get_opinion_ranking(
    sort_by: str = Query("price", description="排序方式"),
    limit: int = Query(10, description="返回数量限制"),
    offset: int = Query(0, description="偏移量"),
    db: Session = Depends(get_db),
):
    """获取观点排行榜"""
    try:
        result = OpinionService.get_opinion_ranking(db, sort_by, limit, offset)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get opinion ranking: {str(e)}",
        )


@router.get("/user/{user_address}", response_model=List[OpinionResponse])
def get_user_opinions(user_address: str, db: Session = Depends(get_db)):
    """获取用户的所有观点"""
    try:
        return OpinionService.get_opinions_by_address(db, user_address)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user opinions: {str(e)}",
        )


@router.get("/detail/{opinion_id}", response_model=OpinionResponse)
def get_opinion(opinion_id: int, db: Session = Depends(get_db)):
    """获取观点详情"""
    opinion = OpinionService.get_opinion(db, opinion_id)
    if not opinion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Opinion not found"
        )
    return opinion


@router.get("/detail/{opinion_id}/price")
def get_opinion_price(opinion_id: int, db: Session = Depends(get_db)):
    """获取观点价格"""
    try:
        price_info = OpinionService.evaluate_opinion_price(db, opinion_id)
        if not price_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Opinion not found"
            )
        return price_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get opinion price: {str(e)}",
        )

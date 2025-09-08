from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.models import (
    MintNFTRequest,
    MintNFTResponse,
    TransferNFTRequest,
    TransferNFTResponse,
    NFTListResponse,
    PurchaseNFTRequest,
    PurchaseNFTResponse,
)
from app.services.nft_service import NFTService
from app.utils.jwt_auth import authenticate
from app.database import get_db
from typing import List


router = APIRouter()


@router.post("/mint", response_model=MintNFTResponse)
def mint_nft(
    request: MintNFTRequest,
    address: str = Depends(authenticate),
    db: Session = Depends(get_db),
):
    """将观点铸造为NFT"""
    try:
        result = NFTService.mint_nft(db, request.opinion_id, address)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result.error
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mint NFT: {str(e)}",
        )


@router.get("/mint/estimate")
def get_mint_estimate(
    opinion_id: int = Query(..., description="观点ID"),
    db: Session = Depends(get_db)
):
    """获取NFT铸造估价"""
    try:
        estimate = NFTService.get_mint_estimate(db, opinion_id)
        return estimate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get mint estimate: {str(e)}",
        )


@router.get("/purchase/estimate")
def get_purchase_estimate(
    nft_id: int = Query(..., description="NFT ID"),
    db: Session = Depends(get_db)
):
    """获取NFT购买估价"""
    try:
        estimate = NFTService.get_purchase_estimate(db, nft_id)
        return estimate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get purchase estimate: {str(e)}",
        )


@router.post("/purchase", response_model=PurchaseNFTResponse)
def purchase_nft(
    request: PurchaseNFTRequest,
    address: str = Depends(authenticate),
    db: Session = Depends(get_db),
):
    """购买NFT"""
    try:
        result = NFTService.purchase_nft(db, request.nft_id, address)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result.error
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to purchase NFT: {str(e)}",
        )


@router.post("/transfer", response_model=TransferNFTResponse)
def transfer_nft(
    request: TransferNFTRequest,
    address: str = Depends(authenticate),
    db: Session = Depends(get_db),
):
    """转移NFT所有权"""
    try:
        result = NFTService.transfer_nft(
            db, request.nft_id, address, request.to_address
        )
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=result.error
            )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to transfer NFT: {str(e)}",
        )


@router.get("/user/{user_address}", response_model=List[NFTListResponse])
def get_user_nfts(user_address: str, db: Session = Depends(get_db)):
    """获取用户拥有的NFT列表"""
    try:
        return NFTService.get_user_nfts(db, user_address)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user NFTs: {str(e)}",
        )

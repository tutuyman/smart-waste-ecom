from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.orm import selectinload

from database.db import get_db_session
from database.models import Bid, Product, User

from handler.user import jwt_auth_required
from datetime import datetime

router = APIRouter()

class ProductResponse(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    stock: int
    expiry_date: datetime
    product_cost: int
    retail_price: int
    offer_price: Optional[int]
    discount: Optional[float]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d')  # Serialize datetime to ISO format
        }

class BidResponse(BaseModel):
    id: int
    product_id: str
    user_id: int
    offer_price: Optional[int]
    quantity: Optional[int]
    status: str

    product: Optional[ProductResponse]

@router.get("/api/bids", response_model=List[BidResponse])
def get_bids(
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]

    session = get_db_session()

    bids: List[Bid] = []
    bid_responses: List[BidResponse] = []
    match role:
        case "ADMIN":
            bids = session.exec(select(Bid)).all()

            for bid in bids:
                for offer in bid.product.product_offers:
                    if offer.user_id != bid.user_id :
                        continue

                    res = BidResponse(**bid.dict())
                    res.product = ProductResponse(**bid.product.dict())
                    res.product.offer_price = offer.offer_price
                    res.product.discount = offer.discount
                    bid_responses.append(res)

        case "USER":
            bids = session.exec(
                select(Bid)
                    .where(Bid.user_id == user_id)
                    .options(selectinload(Bid.product))
            ).all()

            for bid in bids:
                res = BidResponse(**bid.dict())
                res.product = ProductResponse(**bid.product.dict())
                for offer in bid.product.product_offers:
                    if not offer.user_id == user_id:
                        continue
                    res.product.offer_price = offer.offer_price
                    res.product.discount = offer.discount
                    break
                bid_responses.append(res)

        case default:
            raise HTTPException(status_code=400, detail={"detail": "invalid role"})

    return bid_responses


class SubmitBidRequest(BaseModel):
    product_id: str
    offer_price: int
    quantity: int

@router.post("/api/bids")
def submit_bid(
    request: SubmitBidRequest,
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]
    
    print(auth)

    session = get_db_session()

    product = session.exec(select(Product).where(Product.id == request.product_id)).one_or_none()
    if product == None:
        raise HTTPException(status_code=400, detail={"detail": "invalid product_id"})


    bid = Bid(product_id=request.product_id, user_id=user_id, quantity=request.quantity, offer_price=request.offer_price, status="PENDING")
    session.add(bid)
    session.commit()

    return {
        "message": "bid successfully sent"
    }

@router.post("/api/bids/{bid_id}/accept")
def accept_bid(
    bid_id: int,
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]
    
    print("amba")
    print(auth)

    if role != "ADMIN":
        raise HTTPException(status_code=403, detail={"detail": "require admin role"})
    
    session = get_db_session()
    
    bid = session.exec(select(Bid).where(Bid.id == bid_id)).one_or_none()
    if bid == None:
        raise HTTPException(status_code=404, detail={"detail": "bid not found"})
    
    bid.status = "ACCEPTED"
    session.add(bid)
    session.commit()
    
    return {
        "message": "bid successfully approved"
    }

@router.post("/api/bids/{bid_id}/reject")
def rejected_bid(
    bid_id: int,
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]

    if role != "ADMIN":
        raise HTTPException(status_code=403, detail={"detail": "require admin role"})

    session = get_db_session()
    bid = session.exec(select(Bid).where(Bid.id == bid_id)).one_or_none()
    if bid == None:
        raise HTTPException(status_code=404, detail={"detail": "bid not found"})

    bid.status = "REJECTED"
    session.add(bid)
    session.commit()
    
    return {
        "message": "bid successfully rejected"
    }

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import select, alias
from sqlalchemy.orm import selectinload, joinedload
from datetime import datetime

from database.db import get_db_session
from database.models import Product, ProductOffer

from handler.user import jwt_auth_required

router = APIRouter()

class ProductOfferResponse(BaseModel):
    user_id: int
    offer_price: int
    discount: float


class ProductResponse(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    stock: int
    expiry_date: datetime
    product_cost: int
    retail_price: int
    product_offers: List[ProductOfferResponse]

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d')  # Serialize datetime to ISO format
        }

@router.get("/api/product-offers", response_model=List[ProductResponse])
def get_product_offers(
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]

    session = get_db_session()

    products: List[Product] = []

    match role:
        case "USER":
            products = session.exec(
                select(Product)
                    .join(ProductOffer)
                    .where(ProductOffer.user_id == int(user_id))
            ).all()

            product_offers = session.exec(
                select(ProductOffer)
                    .where(ProductOffer.user_id == int(user_id))
            ).all()

            res: List[ProductResponse] =  []
            for p in products:
                offers = [ProductOfferResponse(**offer.dict()) for offer in product_offers if offer.product_id == p.id]
                res.append(ProductResponse(**p.dict(), product_offers=offers))

            return res
        case "ADMIN":
            products = session.exec(
                select(Product).options(selectinload(Product.product_offers))
            ).all()

            res: List[ProductResponse] =  []
            for p in products :
                product_offers = [ProductOfferResponse(**po.dict()) for po in p.product_offers]
                res.append(ProductResponse(**p.dict(), product_offers=product_offers))

            return res
        case default:
            raise HTTPException(status_code=400, detail={"detail": "invalid role"})


@router.get("/api/products", response_model=List[Product])
def get_products(
    auth = Depends(jwt_auth_required),
):
    user_id = auth["user_id"]
    role = auth["role"]

    session = get_db_session()

    products: List[Product] = []

    match role:
        case "USER":
            products = session.exec(
                select(Product)
                    .join(ProductOffer)
                    .where(ProductOffer.user_id == int(user_id))
            ).all()

        case "ADMIN":
            products = session.exec(
                select(Product)
            ).all()
        case default:
            raise HTTPException(status_code=400, detail={"detail": "invalid role"})

    return products

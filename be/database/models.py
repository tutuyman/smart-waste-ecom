from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    role: str  # Enum('USER', 'ADMIN')

    # Relationships
    product_offers: List["ProductOffer"] = Relationship(back_populates="user")
    bids: List["Bid"] = Relationship(back_populates="user")


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: str = Field(default=None, primary_key=True)
    name: str
    brand: str
    category: str
    stock: int
    expiry_date: datetime = Field(default=None)  # Can store timestamp or datetime as string
    product_cost: int
    retail_price: int

    # Relationships
    product_offers: List["ProductOffer"] = Relationship(back_populates="product")
    bids: List["Bid"] = Relationship(back_populates="product")


class ProductOffer(SQLModel, table=True):
    __tablename__ = "product_offer"

    user_id: int = Field(default=None, foreign_key="users.id", primary_key=True)
    product_id: str = Field(default=None, foreign_key="products.id", primary_key=True)
    offer_price: int
    discount: float

    # Relationships
    user: User = Relationship(back_populates="product_offers")
    product: Product = Relationship(back_populates="product_offers")


class Bid(SQLModel, table=True):
    __tablename__ = "bids"

    id: int = Field(default=None, primary_key=True)
    product_id: str = Field(default=None, foreign_key="products.id")
    user_id: int = Field(default=None, foreign_key="users.id")
    offer_price: int
    quantity: int
    status: str

    # Relationships
    product: Product = Relationship(back_populates="bids")
    user: User = Relationship(back_populates="bids")

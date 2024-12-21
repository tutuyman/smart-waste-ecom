from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from handler.user import router as user_router
from handler.product import router as product_router
from handler.bid import router as bid_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(bid_router)

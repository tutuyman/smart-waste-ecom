from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from sqlmodel import select
from database.models import User
from database.db import get_db_session

import jwt
import bcrypt

# Define a secret key for encoding the JWT
SECRET_KEY = "hardcoded_secret"

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/token")
def login(credentials: LoginRequest):
    session = get_db_session()

    user = session.exec(select(User).where(User.username == credentials.username)).one_or_none()
    if user == None :
        raise HTTPException(status_code=403, detail={"detail": "Invalid username or password"})

    # Check password using bcrypt
    if not bcrypt.checkpw(credentials.password.encode(), user.password.encode()):
        raise HTTPException(status_code=403, detail="Invalid username or password")


    # Create JWT
    access_token = jwt.encode(
        {
            "username": user.username,
            "user_id": user.id,
            "role": user.role,
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return {
        "access_token": access_token,
        "username": user.username,
        "user_id": user.id,
        "role": user.role,
    }


def verify_jwt(token: str):
    """
    Decodes the JWT token and verifies its integrity.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp":False})
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# JWT Authentication Scheme
auth_scheme = HTTPBearer()

def jwt_auth_required(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Dependency function to enforce JWT Bearer authentication.
    Returns the decoded payload if the token is valid.
    """
    return verify_jwt(credentials.credentials)



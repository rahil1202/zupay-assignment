from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel

from utils import password, jwt
from models.User import Users


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.verify_access_token(token)

    if payload is None:
        raise credentials_exception

    email: str = payload.get("email")
    if not email:
        raise credentials_exception

    user = Users.find_one_by({"email": email})

    if not user:
        raise credentials_exception

    return user

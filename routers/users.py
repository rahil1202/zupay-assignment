from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from bson.objectid import ObjectId
from slugify import slugify
from typing import Annotated
from random import randbytes

from models.User import User, Users
from utils import password, jwt
from middlewares import auth

router = APIRouter()


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    tags: list[str]


@router.post("/create")
async def create_user(user: CreateUser):
    user = User(**user.model_dump())

    user.id_slug = slugify(user.name, max_length=20) + "-" + randbytes(3).hex().lower()
    user.email = user.email.lower()

    if Users.find_one_by({"email": user.email}):
        raise HTTPException(400, "User already exists")

    user.password = password.hash_password(user.password)

    Users.save(user)

    access_token = jwt.create_access_token({"email": user.email})
    refresh_token = jwt.create_refresh_token({"email": user.email})

    return {
        "user": user.model_dump(exclude=["password"]),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/login")
async def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = Users.find_one_by(
        {
            "$or": [
                {"email": credentials.username.lower()},
                {"id": credentials.username.upper()},
            ]
        }
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not password.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = jwt.create_access_token({"email": user.email})
    refresh_token = jwt.create_refresh_token({"email": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh_token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode_refresh_token(refresh_token)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = Users.find_one_by({"email": payload["email"]})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = jwt.create_access_token({"email": user.email})
    refresh_token = jwt.create_refresh_token({"email": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


class PublicUser(BaseModel):
    id: str
    name: str
    email: str
    tags: list[str]


@router.get("/me")
async def me(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return PublicUser(**current_user.model_dump())


class UpdateUser(BaseModel):
    name: str | None = None
    tags: list[str] | None = None
    tags_add: list[str] | None = None
    tags_remove: list[str] | None = None


@router.patch("/update")
async def update_user(
    current_user: Annotated[User, Depends(auth.get_current_user)], user: UpdateUser
):
    update_data = user.model_dump(exclude_unset=True)
    new_tags = []
    if "tags" in update_data:
        new_tags = update_data.pop("tags")
    elif "tags_add" in update_data:
        new_tags = current_user.tags.copy()
        for tag in update_data.pop("tags_add"):
            if tag not in new_tags:
                new_tags.append(tag)
    elif "tags_remove" in update_data:
        new_tags = [
            tag
            for tag in current_user.tags
            if tag not in update_data.pop("tags_remove")
        ]

    if len(new_tags) != 0:
        update_data["tags"] = new_tags
    else:
        update_data.pop("tags")

    update_user = current_user.model_copy(update=update_data)

    Users.save(update_user)

    return PublicUser(**update_user.model_dump(exclude=["password"]))


@router.delete("/delete")
async def delete_user(current_user: Annotated[User, Depends(auth.get_current_user)]):
    Users.delete(current_user)

    return PublicUser(**current_user)


@router.get("/all")
async def get_all_users():
    return [PublicUser(**user.model_dump()) for user in Users.find_by({})]

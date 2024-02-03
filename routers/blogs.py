from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from models.Blog import Author, Blog, Blogs
from typing import Annotated
from pydantic import BaseModel
from slugify import slugify
from random import randbytes

from models.User import User
from middlewares import auth

router = APIRouter()


@router.get("/")
async def get_all_blogs(
    page_size: int = 10, page_index: int = 1, query: str | None = None
):
    search = {}

    if query is not None:
        search = {"$text": {"$search": query, "$caseSensitive": False}}

    blogs = (
        Blogs.get_collection()
        .find(search)
        .sort("last_modified", -1)
        .skip(page_size * (page_index - 1))
        .limit(page_size)
    )

    blogs = [Blog(**blog, id=str(blog["_id"])) for blog in list(blogs)]

    return blogs


class CreateBlog(BaseModel):
    title: str
    content: str
    tags: list[str]


@router.post("/create")
async def create_blog(
    current_user: Annotated[User, Depends(auth.get_current_user)], blog: CreateBlog
):
    new_blog = Blog(
        id_slug=slugify(blog.title, max_length=20) + "-" + randbytes(3).hex().lower(),
        title=blog.title,
        content=blog.content,
        author=Author(**current_user.model_dump()),
        tags=blog.tags,
        last_modified=datetime.now(),
    )

    Blogs.save(new_blog)

    return new_blog


@router.get("/{id_slug}")
async def get_blog(id_slug: str):
    blog = Blogs.find_one_by({"id_slug": id_slug})

    return blog


class UpdateBlog(BaseModel):
    title: str | None
    content: str | None
    tags: list[str] | None


@router.patch("/{id_slug}")
async def update_blog(
    id_slug: str,
    current_user: Annotated[User, Depends(auth.get_current_user)],
    blog: UpdateBlog,
):
    existing_blog = Blogs.find_one_by(
        {"id_slug": id_slug, "author.id_slug": current_user.id_slug}
    )

    if not existing_blog:
        raise HTTPException(404, "Blog not found or does not belong to you")

    update_data = blog.model_dump(exclude_unset=True)
    updated_blog = existing_blog.model_copy(update=update_data)

    Blogs.save(updated_blog)

    return updated_blog


@router.delete("/{id_slug}")
async def delete_blog(
    id_slug: str,
    current_user: Annotated[User, Depends(auth.get_current_user)],
):
    existing_blog = Blogs.find_one_by(
        {"id_slug": id_slug, "author.id_slug": current_user.id_slug}
    )

    if not existing_blog:
        raise HTTPException(404, "Blog not found or does not belong to you")

    Blogs.delete(existing_blog)

    return existing_blog


@router.post("/personalized")
async def get_personalized_blogs(
    current_user: Annotated[User, Depends(auth.get_current_user)]
):
    user_tags = current_user.tags

    blogs = Blogs.get_collection().aggregate(
        [
            {
                "$project": {
                    "id": "$_id",
                    "id_slug": 1,
                    "author": 1,
                    "title": 1,
                    "content": 1,
                    "tags": 1,
                    "last_modified": 1,
                    "intersection": {
                        "$size": {"$setIntersection": [user_tags, "$tags"]}
                    },
                },
            },
            {
                "$sort": {"intersection": -1, "last_modified": -1},
            },
        ]
    )

    return [Blog(**blog) for blog in list(blogs)]

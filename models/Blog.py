from datetime import datetime
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from pymongo import IndexModel, TEXT
from database import db_client


class Author(BaseModel):
    id_slug: str
    name: str


class Blog(BaseModel):
    id: ObjectIdField | None = None
    id_slug: str
    title: str
    content: str
    author: Author
    tags: list[str]
    last_modified: datetime


class BlogRepository(AbstractRepository[Blog]):
    class Meta:
        collection_name = "blogs"


Blogs = BlogRepository(database=db_client)

Blogs.get_collection().create_index(
    [("id_slug", TEXT), ("author.id_slug", TEXT), ("tags", TEXT), ("title", TEXT)]
)

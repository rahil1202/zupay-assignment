from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField

from database import db_client


class User(BaseModel):
    id: ObjectIdField | None = None
    id_slug: str | None = None
    name: str
    email: str
    password: str
    tags: list[str]


class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = "users"


Users = UserRepository(database=db_client)

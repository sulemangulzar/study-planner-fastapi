from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default=None, primary_key=True)
    name: str = Field()
    email: EmailStr = Field()
    password_hash: str = Field()

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from models.book import Book

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str = Field(index=True)


books: list["Book"] = Relationship(back_populates="owner")

class UserCreate(SQLModel):
    name: str
    email: str
    college: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    college: Optional[str] = None

class UserDelete(SQLModel):
    id: int


User.model_rebuild()    
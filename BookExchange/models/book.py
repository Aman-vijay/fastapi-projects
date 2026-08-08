from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_available: bool = Field(default=True)
    is_sold: bool = Field(default=False)

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


class BookCreate(SQLModel):
    title: str
    author: str
    price: int
    owner_id: int

class BookRead(SQLModel):
    id: int
    title: str
    author: str
    price: int
    owner_id: int
    is_available: bool
    is_sold: bool

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None
    is_sold: Optional[bool] = None

class BookDelete(SQLModel):
    id: int


Book.model_rebuild()

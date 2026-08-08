from fastapi import APIRouter,Depends,HTTPException,Query
from typing import Optional
from sqlmodel import Session,select
from db import get_session
from models.book import Book,BookCreate,BookRead,BookUpdate
from auth import verify_api_key
import os

books_router = APIRouter(prefix="/books",tags=["books"])

#Rest Api for book
#Listing all books
@books_router.get("/",response_model=list[BookRead])
def list_books(
    title: Optional[str] = Query(default=None,description="Title of the book"),
    author: Optional[str] = Query(default=None,description="Author of the book"),
    session: Session = Depends(get_session),
):
    query = select(Book).where(
        Book.is_available == True,
    )

    if title:
        query = query.where(Book.title.contains(title))
    if author:
        query = query.where(Book.author.contains(author))

    books = session.exec(query).all()
    return books

@books_router.post("/",response_model=BookRead)
def create_book(book:BookCreate,session:Session=Depends(get_session),api_key:str=Depends(verify_api_key)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401,detail="Invalid API key")
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

#Rest Api for patch book
@books_router.patch("/{book_id}",response_model=BookRead)
def update_book(
    book_id: int,
    updates: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401,detail="Invalid API key")
    db_book = session.get(Book,book_id)
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    updates_data = updates.model_dump(exclude_unset=True)
    for key,value in updates_data.items():
        setattr(db_book,key,value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

#Rest Api for delete book
@books_router.delete("/{book_id}",status_code=204)
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401,detail="Invalid API key")
    db_book = session.get(Book,book_id)
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"message": "Book deleted successfully"}


@books_router.patch("/{book_id}/sell",response_model=BookRead)
def sell_book(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401,detail="Invalid API key")
    db_book = session.get(Book,book_id)
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    db_book.is_sold = True
    db_book.is_available = False
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

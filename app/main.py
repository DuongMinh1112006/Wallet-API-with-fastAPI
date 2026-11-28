from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import Base, engine, SessionLocal
from models import Book
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookCreate(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    book = Book(
        title=book_data.title,
        author=book_data.author
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author
    }


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    statement = select(Book)
    books = db.scalars(statement).all()
    return books
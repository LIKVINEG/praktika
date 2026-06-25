import sys
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import crud, models, db as db_config
from app import schemas

app = FastAPI(title="Bookstore API", description="API для управления книгами и категориями")

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "alive", "database": "connected"}


@app.post("/categories", response_model=schemas.CategoryResponse, tags=["Categories"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(db_config.get_db)):
    return crud.create_category(db=db, title=category.title)

@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Categories"])
def read_categories(db: Session = Depends(db_config.get_db)):
    return crud.get_all_categories(db)

@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(db_config.get_db)):
    deleted = crud.delete_category(db, category_id=category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": f"Category {category_id} successfully deleted"}


@app.post("/books", response_model=schemas.BookResponse, tags=["Books"])
def create_book(book: schemas.BookCreate, db: Session = Depends(db_config.get_db)):
    category = crud.get_category_by_id(db, category_id=book.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    return crud.create_book(
        db=db, 
        title=book.title, 
        description=book.description, 
        price=book.price, 
        category_id=book.category_id, 
        url=book.url
    )

@app.get("/books", response_model=List[schemas.BookResponse], tags=["Books"])
def read_books(db: Session = Depends(db_config.get_db)):
    return crud.get_all_books(db)

@app.put("/books/{book_id}", response_model=schemas.BookResponse, tags=["Books"])
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(db_config.get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, book_id=book_id, book_data=book.model_dump())

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(db_config.get_db)):
    deleted = crud.delete_book(db, book_id=book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book {book_id} successfully deleted"}
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db import crud, db as db_config
from app import schemas

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(db_config.get_db)):
    # Валидация бизнес-логики: проверяем, существует ли категория
    category = crud.get_category_by_id(db, category_id=book.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Category with id {book.category_id} does not exist"
        )
    return crud.create_book(
        db=db, 
        title=book.title, 
        description=book.description, 
        price=book.price, 
        category_id=book.category_id, 
        url=book.url
    )

@router.get("", response_model=List[schemas.BookResponse])
def read_books(category_id: Optional[int] = Query(None, description="Фильтр по ID категории"), db: Session = Depends(db_config.get_db)):
    if category_id is not None:
        return crud.get_books_by_category(db, category_id=category_id)
    return crud.get_all_books(db)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(db_config.get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(db_config.get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    category = crud.get_category_by_id(db, category_id=book.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Category with id {book.category_id} does not exist"
        )
        
    return crud.update_book(db, book_id=book_id, book_data=book.model_dump())

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(db_config.get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    crud.delete_book(db, book_id=book_id)
    return {"message": f"Book {book_id} successfully deleted"}
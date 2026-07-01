from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db import crud, db as db_config
from app import schemas

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(db_config.get_db)):
    return crud.create_category(db=db, title=category.title)

@router.get("", response_model=List[schemas.CategoryResponse])
def read_categories(db: Session = Depends(db_config.get_db)):
    return crud.get_all_categories(db)

@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def read_category(category_id: int, db: Session = Depends(db_config.get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(db_config.get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return crud.update_category(db, category_id=category_id, title=category.title)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(db_config.get_db)):
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    crud.delete_category(db, category_id=category_id)
    return {"message": f"Category {category_id} successfully deleted"}
from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = ""

class BookCreate(BookBase):
    category_id: int

class BookResponse(BookBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    books: List[BookResponse] = []

    class Config:
        from_attributes = True
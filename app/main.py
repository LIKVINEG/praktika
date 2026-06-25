import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db import crud

def main():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("ВЫВОД ДАННЫХ ИЗ БАЗЫ ДАННЫХ POSTGRESQL:")
        print("=" * 50)
        
        books = crud.get_all_books(db)
        for book in books:
            print(f"Книга: '{book.title}'")
            print(f"Категория: {book.category.title}")
            print(f"Описание: {book.description}")
            print(f"Цена: {book.price} руб.")
            print("-" * 50)
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
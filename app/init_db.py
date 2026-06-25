import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import engine, Base, SessionLocal
from app.db import crud

def init():
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        existing = crud.get_all_categories(db)
        if not existing:
            print("Наполнение базы данных начальными данными...")
            cat_it = crud.create_category(db, title="Программирование")
            cat_fiction = crud.create_category(db, title="Фантастика")
            
            crud.create_book(db, title="Изучаем Python", description="Классический учебник Марка Лутца", price=2500.0, category_id=cat_it.id)
            crud.create_book(db, title="Чистый код", description="Руководство по рефакторингу Роберта Мартина", price=1200.0, category_id=cat_it.id)
            
            crud.create_book(db, title="Дюна", description="Культовый роман Фрэнка Герберта", price=850.0, category_id=cat_fiction.id)
            crud.create_book(db, title="Основание", description="Цикл романов Айзека Азимова", price=950.0, category_id=cat_fiction.id)
            
            print("База успешно инициализирована!")
        else:
            print("База данных уже содержит информацию.")
    finally:
        db.close()

if __name__ == "__main__":
    init()
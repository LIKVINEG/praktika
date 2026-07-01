import sys
import os
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import categories, books

app = FastAPI(title="Bookstore API", description="API для управления книгами и категориями")

app.include_router(categories.router)
app.include_router(books.router)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "alive", "database": "connected"}
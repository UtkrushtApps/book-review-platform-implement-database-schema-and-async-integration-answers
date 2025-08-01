from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from . import models, schemas, crud
from .database import engine, Base, get_db

app = FastAPI()

# --- Optional: DB Initialization endpoint ---
@app.on_event("startup")
async def on_startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_user = await crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user

@app.post("/books/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.create_book(db, book)
    return db_book

@app.post("/reviews/", response_model=schemas.ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_review = await crud.create_review(db, review)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_review

@app.get("/reviews/{review_id}", response_model=schemas.ReviewRead)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    db_review = await crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.get("/books/{book_id}/reviews", response_model=List[schemas.ReviewRead])
async def get_reviews_by_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_reviews_by_book(db, book_id)

@app.get("/users/{user_id}/reviews", response_model=List[schemas.ReviewRead])
async def get_reviews_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_reviews_by_user(db, user_id)

@app.get("/reviews/", response_model=List[schemas.ReviewRead])
async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_reviews(db)

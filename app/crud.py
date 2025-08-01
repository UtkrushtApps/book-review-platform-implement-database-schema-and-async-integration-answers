from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select as sync_select
from . import models, schemas
from typing import List, Optional
from sqlalchemy.orm import joinedload

# User
async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise ValueError("Username already exists")

async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()

# Book
async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    return result.scalars().first()

# Review CRUD
async def create_review(db: AsyncSession, review: schemas.ReviewCreate) -> models.Review:
    # Ensure user and book exist
    user = await get_user(db, review.user_id)
    book = await get_book(db, review.book_id)
    if not user:
        raise ValueError("User not found")
    if not book:
        raise ValueError("Book not found")
    # Check for unique review by user for this book
    stmt = select(models.Review).where(
        models.Review.user_id == review.user_id,
        models.Review.book_id == review.book_id
    )
    res = await db.execute(stmt)
    if res.scalars().first():
        raise ValueError("User has already reviewed this book.")
    db_review = models.Review(
        content=review.content,
        user_id=review.user_id,
        book_id=review.book_id
    )
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_review(db: AsyncSession, review_id: int) -> Optional[models.Review]:
    res = await db.execute(select(models.Review).where(models.Review.id == review_id))
    return res.scalars().first()

async def get_reviews_by_book(db: AsyncSession, book_id: int) -> List[models.Review]:
    stmt = select(models.Review).options(joinedload(models.Review.user)).where(models.Review.book_id == book_id)
    res = await db.execute(stmt)
    return res.scalars().all()

async def get_reviews_by_user(db: AsyncSession, user_id: int) -> List[models.Review]:
    stmt = select(models.Review).options(joinedload(models.Review.book)).where(models.Review.user_id == user_id)
    res = await db.execute(stmt)
    return res.scalars().all()

async def get_all_reviews(db: AsyncSession) -> List[models.Review]:
    stmt = select(models.Review)
    res = await db.execute(stmt)
    return res.scalars().all()

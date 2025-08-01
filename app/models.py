from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)

    reviews = relationship('Review', back_populates='user', cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)

    reviews = relationship('Review', back_populates='book', cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='user_book_unique_review'),
    )
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), nullable=False)

    user = relationship('User', back_populates='reviews')
    book = relationship('Book', back_populates='reviews')

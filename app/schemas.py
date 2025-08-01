from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., max_length=100)

class UserRead(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=100)

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    content: str = Field(..., min_length=1)

class ReviewRead(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    book_id: int
    class Config:
        orm_mode = True

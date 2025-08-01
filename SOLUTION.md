# Solution Steps

1. 1. Design the database schema: three tables - users, books, and reviews. Users have id and username; books have id, title, and author; reviews have id, content, created_at, user_id (FK), book_id (FK), and unique constraint on (user_id, book_id).

2. 2. Implement SQLAlchemy ORM models for User, Book, and Review, including foreign keys and relationships, using a shared declarative Base.

3. 3. Create Pydantic schemas for user, book, and review creation and reading, ensuring proper field types and validation.

4. 4. Set up database connection using SQLAlchemy async engine, sessionmaker, and a Base class for ORM models. Provide get_db dependency for FastAPI endpoints.

5. 5. Implement async CRUD functions in crud.py: create_user, get_user, create_book, get_book, create_review (with validation and unique checks), get_review, get_reviews_by_book, get_reviews_by_user, get_all_reviews.

6. 6. Integrate CRUD functions into FastAPI endpoints in main.py for creating users, books, reviews and fetching reviews by book, user, all, or single review. Handle errors with HTTP exceptions and map responses to schemas.

7. 7. (Optional but recommended) Add an on_startup event handler to run database migrations or create tables on FastAPI startup (for simplicity, use run_sync with Base.metadata.create_all).

8. 8. Test endpoints for user/book creation, posting reviews, and querying reviews to confirm persistence and async integration with PostgreSQL.


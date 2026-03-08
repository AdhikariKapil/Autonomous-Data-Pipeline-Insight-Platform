from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models_db import Book
from models.schema import BookCreate, BookUpdate


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author: Optional[str] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_rating: Optional[float] = None,
):
    """
    Get all books with optinal filters
    """
    query = db.query(Book)  # Start a query that selects data from Book table.

    if author:
        author_lower = author.lower()
        query = query.filter(Book.author.ilike(f"%{author_lower}%"))

    if min_year:
        query = query.filter(Book.year >= min_year)

    if max_year:
        query = query.filter(Book.year <= max_year)

    if min_rating:
        query = query.filter(Book.rating >= min_rating)

    return query.offset(skip).limit(limit).all()


def get_specific_book(db: Session, book_id: int):
    """
    Get a book by specific id
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        return book


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_update: BookUpdate):
    db_book = get_specific_book(db, book_id)
    if not db_book:
        return None

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_specific_book(db, book_id)
    if not db_book:
        return None

    db.delete(db_book)
    db.commit()
    return db_book


def get_book_status(db: Session):
    total = db.query(Book).count()
    avg_rating = db.query(func.avg(Book.rating)).scalar()
    oldest = db.query(Book).order_by(Book.year).first()
    newest = db.query(Book).order_by(Book.year.desc()).first()

    return {
        "total_books": total,
        "average_rating": round(avg_rating, 2) if avg_rating else None,
        "oldest_book": (
            {"title": {oldest.title}, "year": {oldest.year}} if oldest else None
        ),
        "newest_book": (
            {"title": {newest.title}, "year": {newest.year}} if newest else None
        ),
    }

from fastapi import FastAPI, HTTPException, Query, Path, Depends, status, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models.schema import BookCreate, BookResponse, BookUpdate
from services.crud import (
    get_books,
    get_specific_book,
    create_book,
    update_book,
    delete_book,
    get_book_status,
)

app = FastAPI(
    title="Book Store API",
    description="API for managing book store with Postgres database",
    version="1.0.0",
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@app.get("/")
async def root():
    return {
        "message": "📚 Book Store API",
        "docs": "/docs",
        "database": "PostgreSQL (running in Docker)",
    }


@app.get("/books", response_model=List[BookResponse])
async def read_book(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    author: Optional[str] = Query(None, description="Filter by Author"),
    min_year: Optional[int] = Query(None, ge=1000, le=2026),
    max_year: Optional[int] = Query(None, ge=1000, le=2026),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    db: Session = Depends(get_db),
):
    """
    Get all book optinally filtered
    """
    books = get_books(db, skip, limit, author, min_year, max_year, min_rating)
    return books


@app.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int = Path(..., description="Id of the book to get"),
    db: Session = Depends(get_db),
):
    """
    Get specific book by id
    """
    book = get_specific_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )

    return book


@app.post("/books", response_model=BookResponse)
async def create_new_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Add a new book to the collection
    """
    return create_book(db, book)


@app.put("/books/{book_id}", response_model=BookResponse)
async def update_exisiting_book(
    book_update: BookUpdate,
    book_id: int = Path(..., description="Id of the book to update."),
    db: Session = Depends(get_db),
):
    """
    Update an exisiting book
    """
    updated_book = update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )

    return updated_book


@app.delete("/books/{book_id}")
async def delete_exisiting_book(
    book_id: int = Path(..., description="Id of the book to delete"),
    db: Session = Depends(get_db),
):
    """
    Delete a book.
    """
    book_db = delete_book(db, book_id)
    if not book_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found.",
        )

    return {"message": f"Book '{book_db.title}' deleted successfully."}


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about the book collection
    """
    return get_book_status(db)

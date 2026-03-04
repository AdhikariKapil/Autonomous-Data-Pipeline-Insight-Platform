from fastapi import FastAPI, HTTPException, Query, Path, status
from typing import Optional, List
from datetime import datetime

# model
from models import Book, BookCreate, BookResponse, BookUpdate

app = FastAPI(
    title="My Book Collection API",
    version="0.2.0",
)

# My simple database for learning
# A list to store our book
book_db = []


# add some extra books
sample_books = [
    {
        "id": "book_1",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
        "rating": 4.5,
        "notes": "Classic American novel",
        "genre": "Romance",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": "book_2",
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "rating": 4.8,
        "notes": "Dystopian masterpiece",
        "created_at": datetime.now().isoformat(),
    },
    {
        "id": "book_3",
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "rating": 4.7,
        "notes": "Powerful story about justice",
        "created_at": datetime.now().isoformat(),
    },
]
book_db.extend(sample_books)


# Helper function
def find_book(book_id: str):
    """
    Find a book using id in our database
    """
    for book in book_db:
        if book["id"] == book_id:
            return book
    return None


# ----Api Endpoints----
@app.get("/")
async def root():
    """Welcome Endpoint"""
    return {
        "message": "Welcome to my book collection",
        "endpoints": {
            "GET /books": "List all books",
            "GET /books/{book_id}": "Get a specific book",
            "POST /books": "Add a new book",
            "PUT /books/{book_id}": "Update a book",
            "DELETE /books/{book_id}": "Delete a specific book",
            "GET /books/search/": "Search a book using author or year",
        },
    }


@app.get("/books", response_model=List[BookResponse])
async def list_books(
    author: Optional[str] = Query(None, description="Filter by author"),
    min_year: Optional[int] = Query(None, ge=1000, le=2026),
    max_year: Optional[int] = Query(None, ge=1000, le=2026),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    faviroute: Optional[bool] = Query(None),
):
    """
    Get all books, optionally filtered

    Examples:
    - /books?author=Orwell
    - /books?min_year=1950&max_year=2000
    - /books?min_rating=4.5
    """
    filtered_books = book_db.copy()

    if author:
        author_lower = author.lower()
        filtered_books = [
            b for b in filtered_books if author_lower in b["author"].lower()
        ]

    if min_year:
        filtered_books = [b for b in filtered_books if min_year <= b["year"]]

    if max_year:
        filtered_books = [b for b in filtered_books if max_year >= b["year"]]

    if min_rating:
        filtered_books = [b for b in filtered_books if b.get("rating", 0) >= min_rating]

    if faviroute:
        filtered_books = [b for b in filtered_books if b.get("faviroute") == faviroute]

    return filtered_books


@app.get("/books/{book_id}", response_model=BookResponse)
async def get_specific_book(
    book_id: str = Path(..., description="The id of the book to get")
):
    """
    Get the specific book by ID
    example: /book/book_2
    """
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return book


@app.post("/books", status_code=201)
async def create_book(book: BookCreate):
    """
    Add a new book to the collection
    """
    book_dict = book.model_dump()
    book_id = f"book_{len(book_db) + 1}"
    book_dict["id"] = book_id
    book_dict["created_at"] = datetime.now().isoformat()

    book_db.append(book_dict)

    return {"message": "Successfully added book", "book": book_dict}


@app.put("/books/{book_id}")
async def update_book(
    book_update: BookUpdate,
    book_id: str = Path(..., description="The ID of the book to update"),
):
    """
    Update a book with some or all field.
    """
    # Find the book
    exisiting_book = find_book(book_id)
    if not exisiting_book:
        raise HTTPException(status_code=404, detail="Cannot find exisiting book.")

    # Update only the field that are provided
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            exisiting_book[field] = value

    exisiting_book["updated_at"] = datetime.now().isoformat()
    return {"message": "Updated book Successfully", "book": exisiting_book}


@app.delete("/books/{book_id}")
async def delete_book(book_id: str = Path(..., description="Id of the book to delete")):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found to delete")

    book_db.remove(book)
    return {"message": "Book Deleted Successfully", "book": book}


@app.get("/stats/books")
async def book_stats():
    total_books = len(book_db)
    print(total_books)

    ratings = [
        book.get("rating", 0) for book in book_db if book.get("rating") is not None
    ]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0
    years = [book.get("year") for book in book_db]

    return {
        "total_books": total_books,
        "avg_rating": avg_rating,
        "min_year": min(years),
        "max_year": max(years),
    }

"""
A simple Book Collection API - Learning Pydantic with FastAPI
"""

from pydantic import BaseModel, field_validator, Field
from typing import Optional


class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1000, le=2026)

    # optional field
    rating: Optional[float] = Field(None, ge=0, le=5)
    notes: Optional[str] = Field(None, max_length=1000)
    faviroute: Optional[bool] = False
    genre: Optional[str] = Field(None, max_length=1000)

    # Custom validation
    @field_validator("year")
    @classmethod
    def year_must_be_reasonable(cls, v):
        """
        Make sure the year make sense for the book
        """
        if v < 1800 and v != 0:
            raise ValueError(f"⚠️ Warning: Unusally old book year: {v}")
        return v

    @field_validator("author")
    @classmethod
    def author_name_not_emplty(cls, v):
        """
        Ensure author name is not just whitespace
        """
        if not v.strip():
            raise ValueError("Author name cannot be empty or just spaces.")
        return v.strip()  # To remove extra space

    @field_validator("rating")
    @classmethod
    def rating_not_none_one_decimal_digit(cls, v):
        """
        Ensure that rating is not none and only has 1 decimal place.
        """
        if v is None:
            raise ValueError("Rating cannot be None.")

        if not (v * 10).is_integer():
            raise ValueError(
                f"Rating must have most 1 digit after decimal. Not this: {v}"
            )

        return v


class BookCreate(BaseModel):
    """
    Used when creating a new book
    Same as Book but without auto-generated fields
    """

    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int = Field(..., ge=1000, le=2026)
    rating: Optional[float] = Field(None, ge=0, le=5)
    genre: Optional[str] = None
    faviroute: Optional[bool] = False
    notes: Optional[str] = None


class BookUpdate(BaseModel):
    """
    Used when updating an existing book
    All field are optional because we might update some
    """

    title: Optional[str] = Field(..., min_length=1)
    author: Optional[str] = Field(..., min_length=1)
    year: Optional[int] = Field(..., ge=1000, le=2026)
    rating: Optional[float] = Field(None, ge=0, le=5)
    faviroute: Optional[bool] = False
    notes: Optional[str] = None


class BookResponse(BaseModel):
    """
    What we send back to the user
    """

    id: str
    title: str
    author: str
    year: int
    rating: Optional[float]
    notes: Optional[str] = None
    genre: Optional[str] = None
    faviroute: Optional[bool] = False
    created_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "book_12344",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "year": 1925,
                "rating": 4.5,
                "notes": "Classic Americal novel",
                "faviroute": False,
                "created_at": "2024-01-15T10:30:00",
            }
        }

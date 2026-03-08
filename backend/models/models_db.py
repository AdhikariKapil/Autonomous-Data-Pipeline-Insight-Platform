from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class BookBD(Base):
    """
    SQLAlchemy Model for Books table
    """

    # __tablename__ tells sqlalchemy what to name table in postgres
    __tablename__ = "books"

    # Columns -> These maps to the database columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        """
        How to represent this obj when printed.
        """
        return f"<Book (id={self.id}, title='{self.title}', author='{self.author}')>"

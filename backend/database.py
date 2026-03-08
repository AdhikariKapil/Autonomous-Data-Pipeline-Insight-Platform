from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("Database url cannot be none.")


# Create a database engine
# Engine is the core interface to the database
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to true to see all SQL commands (great for learning)
    pool_size=5,  # Number of connection to keep open
    max_overflow=10,  # Number of extra connection if needed
)

# Create a session factory
# Sessions are what we use to actually talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our model
# All database models will inherit from this
Base = declarative_base()


def get_db():
    """
    Creates a new database session for each request
    Closes it after the request is done
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

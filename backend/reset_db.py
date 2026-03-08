# reset_db.py
from database import engine
from models.models_db import Base

print("⚠️  Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("✅ Tables dropped")

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

print("🏁 Database reset complete")

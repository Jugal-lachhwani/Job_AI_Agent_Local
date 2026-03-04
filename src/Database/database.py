# src/database.py
from sqlmodel import SQLModel, create_engine, Session
from src.models import JobListing, JobAnalysis, SearchHistory  # Import models so SQLModel can create tables

# Using SQLite for simplicity, but easily swappable for PostgreSQL
DATABASE_URL = "sqlite:///./job_agent.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
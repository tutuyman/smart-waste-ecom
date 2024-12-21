from sqlmodel import create_engine, SQLModel, Session
import os

# MySQL Database configuration using environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get the database session
def get_db_session():
    return Session(engine)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.config import settings

# Disable verbose SQLAlchemy query logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Create database engine (echo=False disables SQL query logging)
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False  # Disable SQL logging to reduce noise
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

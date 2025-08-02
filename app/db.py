from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
import os
import logging

# Primary: Remote database from .env, Fallback: Local Podman database
PRIMARY_DATABASE_URL = os.getenv("DATABASE_URL")
FALLBACK_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/user_profile"

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine with fallback support"""
    if PRIMARY_DATABASE_URL:
        try:
            # Try remote database first
            engine = create_engine(PRIMARY_DATABASE_URL, echo=True)
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"Connected to primary database: {PRIMARY_DATABASE_URL.split('@')[1] if '@' in PRIMARY_DATABASE_URL else 'remote'}")
            return engine
        except Exception as e:
            logger.warning(f"☢️ Failed to connect to primary database: {e}")
            logger.info("Falling back to local database...")
    
    # Fallback to local database
    try:
        engine = create_engine(FALLBACK_DATABASE_URL, echo=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Connected to fallback database: localhost:5432")
        return engine
    except Exception as e:
        logger.error(f"Failed to connect to fallback database: {e}")
        raise e

engine = create_database_engine()

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
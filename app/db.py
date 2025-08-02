from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv
import os
import logging

# Load environment variables first
load_dotenv()

# Primary: Remote database from .env, Fallback: Local Podman database
PRIMARY_DATABASE_URL = os.getenv("DATABASE_URL")
FALLBACK_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/user_profile"

logger = logging.getLogger(__name__)

def create_database_engine():
    """Create database engine with fallback support"""
    logger.info(f"🔍 Starting database connection process...")
    logger.info(f"🔍 PRIMARY_DATABASE_URL exists: {PRIMARY_DATABASE_URL is not None}")
    
    if PRIMARY_DATABASE_URL:
        try:
            logger.info(f"🔗 Attempting connection to primary database...")
            # Try remote database first
            engine = create_engine(PRIMARY_DATABASE_URL, echo=True)
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(f"✅ Connected to primary database: {PRIMARY_DATABASE_URL.split('@')[1] if '@' in PRIMARY_DATABASE_URL else 'remote'}")
            return engine
        except Exception as e:
            logger.warning(f"☢️ Failed to connect to primary database: {e}")
            logger.info("🔄 Falling back to local database...")
    else:
        logger.info("ℹ️ No PRIMARY_DATABASE_URL found, going to fallback...")
    
    # Fallback to local database
    try:
        logger.info(f"🔗 Attempting connection to fallback database: {FALLBACK_DATABASE_URL}")
        engine = create_engine(FALLBACK_DATABASE_URL, echo=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Connected to fallback database: localhost:5432")
        return engine
    except Exception as e:
        logger.error(f"❌ Failed to connect to fallback database: {e}")
        raise e

# Lazy initialization - only create engine when needed
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_database_engine()
    return _engine

def init_db():
    SQLModel.metadata.create_all(get_engine())

def get_session():
    with Session(get_engine()) as session:
        yield session
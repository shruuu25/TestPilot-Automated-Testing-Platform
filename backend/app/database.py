import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Setup logger
logger = logging.getLogger("testpilot.database")
logging.basicConfig(level=logging.INFO)

# Load environment variables from backend or root .env
root_dir = Path(__file__).resolve().parent.parent.parent
env_paths = [Path(__file__).resolve().parent.parent / ".env", root_dir / ".env"]
for p in env_paths:
    if p.exists():
        load_dotenv(p)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/testpilot")

def create_app_engine(db_url: str):
    """
    Creates SQLAlchemy engine with automatic fallback handling.
    If MySQL is configured but unavailable, falls back to SQLite so local testing works reliably.
    """
    if db_url.startswith("sqlite"):
        return create_engine(db_url, connect_args={"check_same_thread": False})
    
    try:
        # Test MySQL connection with a short timeout
        test_engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Successfully connected to MySQL database.")
        return test_engine
    except Exception as e:
        logger.warning(
            f"Could not connect to MySQL at '{db_url}': {e}. "
            "Falling back to local SQLite database (sqlite:///./testpilot.db) for zero-dependency execution."
        )
        sqlite_fallback = "sqlite:///./testpilot.db"
        return create_engine(sqlite_fallback, connect_args={"check_same_thread": False})

engine = create_app_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI database dependency yields an isolated session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

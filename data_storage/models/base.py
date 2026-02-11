"""SQLAlchemy declarative base and session utilities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Default to SQLite for development; override via env for production.
def get_engine(url=None):
    import os
    url = url or os.environ.get("DATABASE_URL", "sqlite:///./econodex.db")
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)

def get_session_factory(engine=None):
    engine = engine or get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

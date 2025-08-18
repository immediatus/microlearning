"""
Database configuration and session management
"""

import structlog
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import db_config, settings

logger = structlog.get_logger()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=db_config.ECHO_SQL,
    pool_size=db_config.POOL_SIZE,
    max_overflow=db_config.MAX_OVERFLOW,
    pool_pre_ping=db_config.POOL_PRE_PING,
    pool_recycle=db_config.POOL_RECYCLE,
    poolclass=NullPool if "pytest" in str(settings.DATABASE_URL) else None,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


async def get_db() -> AsyncSession:
    """
    Dependency for getting database session.

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", exc_info=e)
            raise
        finally:
            await session.close()


async def create_tables():
    """Create all database tables."""
    try:
        async with engine.begin() as conn:
            # Import all models to ensure they're registered

            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", exc_info=e)
        raise


async def drop_tables():
    """Drop all database tables (for testing)."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error("Failed to drop database tables", exc_info=e)
        raise


async def check_database_connection():
    """Check if database connection is working."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error("Database connection failed", exc_info=e)
        return False

import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.analytics import AnalyticsEvent
from app.models.billing import AIServiceCost, ApprovalRequest, CreatorBudget
from app.models.content import ContentProject, ContentTag, ContentTemplate, LearningVideo
from app.models.creator import Creator
from app.models.quiz import Quiz, QuizResponse
from app.models.student import Student, StudentPreference, StudentSession


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Create an async engine for the test database."""
    return create_async_engine(TEST_DATABASE_URL, echo=False)

@pytest.fixture(scope="session")
async def tables(engine):
    """Create all tables for the test database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine, tables) -> AsyncSession:
    """Fixture for a database session."""

    connection = await engine.connect()
    transaction = await connection.begin()

    Session = sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )
    session = Session()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()

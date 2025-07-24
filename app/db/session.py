from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    """
    Initializes the database by creating all tables defined
        in the SQLAlchemy Base metadata.
    This asynchronous function establishes a connection to the database engine and runs
    the table creation commands within a transaction. It should be called at application
    startup to ensure the database schema is up to date.
    Raises:
        Any exceptions raised by the database engine or
            SQLAlchemy during table creation.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Asynchronous generator function that provides a database session.
    Yields:
        AsyncSession: An instance of the asynchronous database
            session for use in database operations.
    Usage:
        This function is typically used as a dependency in FastAPI
            routes to provide a database session that is automatically
            closed after the request is completed.
    """

    async with AsyncSessionLocal() as session:
        yield session

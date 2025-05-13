from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import settings

Base = declarative_base()
# for alembic
sync_engine = create_engine(settings.DATABASE_URL, echo=True)
async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True, future=True)


AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionFactory() as session:
            yield session
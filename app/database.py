from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from .settings import settings

engine = create_async_engine(
    settings.sqlalchemy_database_url,
    # connect_args={"check_same_thread": False},
)

async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def get_db():
    async with async_session() as db:
        yield db

        if db.in_transaction():
            await db.commit()

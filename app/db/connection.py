from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from ..settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session  # Yield the session to be used
            await session.commit()  # Commit the session after use
        except Exception as e:
            await session.rollback()  # Rollback if there is an exception
            raise
        finally:
            await session.close()  # Ensure the session is closed

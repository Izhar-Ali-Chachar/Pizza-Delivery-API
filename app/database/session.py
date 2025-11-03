from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from fastapi import Depends

from typing import Annotated

from ..config import settings

engine = create_async_engine(settings.POSTGRES_URL, echo=True)

async def create_tables():
    async with engine.begin() as conn:
        from ..database.models import SQLModel
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

sessionDep = Annotated[AsyncSession, Depends(get_session)]

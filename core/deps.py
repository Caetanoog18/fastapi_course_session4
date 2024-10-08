# Nesse arquivo teremos as dependências que iremos ter no nosso projeto

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session()-> AsyncGenerator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()
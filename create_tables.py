# pgAdmin4 - user: gabriel-caetano e password: python


from core.configs import settings
from core.database import engine

async def create_tables() -> None:
    import models.__all_models
    print('Creating tables in database')

    async with engine.begin() as connection:
        await connection.run_sync(settings.DBBaseModel.metadata.drop_all)
        await connection.run_sync(settings.DBBaseModel.metadata.create_all)

    print('Tables created succefully')

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())

import asyncio
import sys
import os

# Add parent directory to sys.path so Database package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Database.connection import async_engine, Base, check_db_connection
from Database.models import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("krishinetra.db_init")

async def init_database():
    logger.info("Verifying database connectivity...")
    connected = await check_db_connection()
    if not connected:
        logger.warning("Direct check failed or database empty. Proceeding with table creation...")

    logger.info("Creating all 18 relational tables via SQLAlchemy...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Successfully created all 18 database tables:")
    for table_name in Base.metadata.tables.keys():
        logger.info(f" - {table_name}")

    await async_engine.dispose()
    logger.info("Database initialization completed successfully.")

if __name__ == "__main__":
    asyncio.run(init_database())

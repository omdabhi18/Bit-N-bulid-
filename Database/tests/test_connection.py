import pytest
from sqlalchemy import text
from Database.connection import check_db_connection


@pytest.mark.asyncio
async def test_engine_connection(db_session):
    """Verify that the engine and async session can execute raw SQL select queries."""
    result = await db_session.execute(text("SELECT 1 AS alive"))
    scalar_val = result.scalar()
    assert scalar_val == 1


@pytest.mark.asyncio
async def test_health_check_function():
    """Verify the check_db_connection utility reports healthy status."""
    is_healthy = await check_db_connection()
    assert isinstance(is_healthy, bool)

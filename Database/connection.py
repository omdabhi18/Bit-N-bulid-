from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import text
import logging
from Database.config import db_settings

logger = logging.getLogger("krishinetra.database")

class Base(DeclarativeBase):
    pass

# Async Engine (Production async operations & FastAPI)
is_sqlite = "sqlite" in db_settings.DATABASE_URL
async_connect_args = {"check_same_thread": False} if is_sqlite else {}

async_engine = create_async_engine(
    db_settings.DATABASE_URL,
    echo=db_settings.DB_ECHO,
    connect_args=async_connect_args,
    **({} if is_sqlite else {
        "pool_size": db_settings.DB_POOL_SIZE,
        "max_overflow": db_settings.DB_MAX_OVERFLOW,
        "pool_timeout": db_settings.DB_POOL_TIMEOUT,
        "pool_recycle": db_settings.DB_POOL_RECYCLE,
    })
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Sync Engine (for Alembic migrations & sync scripts)
sync_engine = create_engine(
    db_settings.SYNC_DATABASE_URL,
    echo=db_settings.DB_ECHO,
    connect_args={"check_same_thread": False} if "sqlite" in db_settings.SYNC_DATABASE_URL else {}
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def check_db_connection() -> bool:
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error(f"Database connectivity check failed: {e}")
        return False

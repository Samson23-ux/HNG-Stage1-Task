from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


from app.core.config import settings

async_db_engine: AsyncEngine = create_async_engine(
    url=settings.ASYNC_DB_URL,
    connect_args={"server_settings": {"timezone": "utc"}},
    pool_size=5,
    pool_timeout=10.0,
    pool_pre_ping=True,
    max_overflow=3,
)

async_session = async_sessionmaker(
    bind=async_db_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

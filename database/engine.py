"""
Настройка и инициализация подключения к БД
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import config


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Создание движка
engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
    future=True
)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Инициализация БД - создание таблиц"""
    # Импортируем модели, чтобы они были зарегистрированы в Base.metadata
    from database import models  # noqa: F401
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    """Получение сессии БД (async generator)"""
    async with async_session_maker() as session:
        yield session


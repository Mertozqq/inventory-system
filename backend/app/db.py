import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base

# Получение строки подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/data/inventory.db")

# Создание движка SQLAlchemy
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency для FastAPI.
    Возвращает сессию БД и закрывает её после запроса.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Инициализация базы данных (создание таблиц).
    Вызывать один раз при старте или через отдельный скрипт.
    """
    Base.metadata.create_all(bind=engine)

# app/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

print(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # проверка соединений перед использованием
    future=True,
)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ping_db():
    """Простая проверка соединения с БД"""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
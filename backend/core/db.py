from typing import Annotated, Any, Generator
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.core.config import settings
from backend.account.models import Base

DB_USER = settings.DB_USER
DB_PASS = settings.DB_PASS
DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME

url: str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine: Engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]


# Create tables automatically
Base.metadata.create_all(bind=engine)

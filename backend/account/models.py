
from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, String, Uuid, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models.
    This class is used to create the declarative base for the ORM.
    """

    pass


class AbstractBaseModel(Base):
    """
    Abstract base model for all database models.
    This class provides common fields and methods for all models.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), primary_key=True, default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), onupdate=func.now(), default=func.now()
    )


class User(AbstractBaseModel):
    """
    User model for the application.
    This model represents a user in the system.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String(100), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    def __repr__(self) -> str:
        return f"{self.email}>"

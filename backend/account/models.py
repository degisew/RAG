import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Uuid, func, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


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


class DocumentModel(AbstractBaseModel):
    __tablename__ = "documents"

    file_name: Mapped[String] = mapped_column(
        String()
    )

    file_location = mapped_column(
        String()
    )

    def __repr__(self) -> str:
        return f"{self.file_name}"


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

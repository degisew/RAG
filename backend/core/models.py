import uuid
from sqlalchemy import ForeignKey, Uuid, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.account.models import AbstractBaseModel, User


class Document(AbstractBaseModel):
    __tablename__ = "documents"

    file_name: Mapped[String] = mapped_column(
        String()
    )

    file_location = mapped_column(
        String()
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(), ForeignKey("users.id"))

    # Relationships
    organizer: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"{self.file_name}"

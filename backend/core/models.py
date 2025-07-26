from uuid import UUID
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Uuid, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.account.models import AbstractBaseModel, User


class Document(AbstractBaseModel):
    __tablename__ = "documents"

    file_name: Mapped[String] = mapped_column(String())

    file_location = mapped_column(String())

    user_id: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    # Relationships
    organizer: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"{self.file_name}"


class Chat(AbstractBaseModel):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    chat_name: Mapped[str] = mapped_column(String())

    # Relationships
    user: Mapped["User"] = relationship()

    messages: Mapped[list["Message"]] = relationship(back_populates="chat")

    def __repr__(self) -> str:
        return self.chat_name


class Message(AbstractBaseModel):
    __tablename__ = "messages"

    user_id: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("users.id"))

    chat_id: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("chats.id"))

    message: Mapped[str] = mapped_column(String())

    timestamp: Mapped[datetime] = mapped_column(DateTime())

    sender: Mapped[str] = mapped_column(String())

    user: Mapped["User"] = relationship()

    chat: Mapped["Chat"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return self.sender

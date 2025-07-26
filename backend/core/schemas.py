from datetime import datetime
from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ChatSchema(BaseModel):
    query: str
    file_name: str


class DocumentResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    # file_location: str
    file_name: str

    model_config: ConfigDict = {"from_attributes": True}


class BaseMessageSchema(BaseModel):
    sender: Literal["user", "bot"]
    message: str
    timestamp: str  # expect in ISO format from the UI and will do validation
    chatInfo: dict[str, Any]


class MessageResponseSchema(BaseModel):
    id: UUID
    sender: Literal["user", "bot"]
    message: str
    timestamp: datetime

    model_config: ConfigDict = {"from_attributes": True}


class ChatHistoryResponseSchema(BaseModel):
    chat_id: UUID
    chat_name: str

    model_config: ConfigDict = {"from_attributes": True}

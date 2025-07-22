import uuid
from pydantic import BaseModel, ConfigDict


class ChatSchema(BaseModel):
    query: str
    file_name: str


class DocumentResponseSchema(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    # file_location: str
    file_name: str

    model_config: ConfigDict = {"from_attributes": True}

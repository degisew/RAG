from pydantic import BaseModel


class ChatSchema(BaseModel):
    query: str
    file_name: str

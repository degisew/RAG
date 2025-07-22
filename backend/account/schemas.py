import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class BaseUserSchema(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=50)

    model_config: ConfigDict = {"from_attributes": True}


class UserSchema(BaseUserSchema):
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)

    model_config: ConfigDict = {"from_attributes": True}


class UserResponseSchema(BaseUserSchema):
    is_active: bool
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    model_config: ConfigDict = {"from_attributes": True}

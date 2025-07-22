import uuid
from typing import List
from fastapi import APIRouter, status
from backend.account.schemas import (
    UserSchema,
    UserResponseSchema,
)

from backend.account.services import UserService
from backend.core.db import DbSession

router = APIRouter(prefix="/account/users", tags=["Account"])


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(db: DbSession, user: UserSchema) -> UserResponseSchema:
    """
    Create a new user.
    """
    return UserService.create_user(db, user)


@router.get("/")
async def get_users(db: DbSession) -> List[UserResponseSchema]:
    """
    Get all users.
    """
    return UserService.get_users(db)


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
    """
    Get user by ID.
    """
    return UserService.get_user(db, user_id)

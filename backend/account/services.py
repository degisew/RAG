import uuid
from typing import Annotated, Any
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from backend.account.repositories import UserRepository
from backend.core.db import DbSession
from backend.core.config import settings
from backend.account.models import User
from backend.account.schemas import UserResponseSchema, UserSchema
from backend.core.exceptions import (
    AuthenticationErrorException,
    InternalInvariantError,
    NotFoundException,
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY: str = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM

if not SECRET_KEY or not ALGORITHM:
    raise InternalInvariantError(
        "Missing SECRET_KEY or ALGORITHM in .env file.")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

oauth_token_bearer = Annotated[str, Depends(oauth2_scheme)]


class UserService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt_context.hash(password)

    @staticmethod
    def create_user(
        db: DbSession,
        validated_data: UserSchema
    ) -> UserResponseSchema:
        serialized_data: dict[str, Any] = validated_data.model_dump(
            exclude_unset=True, exclude={"confirm_password"}
        )
        password = serialized_data.pop("password")

        if password != validated_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match.",
            )

        hashed_pass = UserService.get_password_hash(password)

        if not hashed_pass:
            raise InternalInvariantError("Password Hashing Failed.")

        serialized_data.update(password=hashed_pass)
        try:
            instance: User = UserRepository.create_user(db, serialized_data)
            return UserResponseSchema.model_validate(instance)
        except SQLAlchemyError as e:
            raise InternalInvariantError(
                f"Database Error while creating user. {str(e)}")

    @staticmethod
    def get_users(db: DbSession) -> list[UserResponseSchema]:
        try:
            users = UserRepository.get_users(db)
            return [UserResponseSchema.model_validate(user) for user in users]
        except SQLAlchemyError as e:
            raise InternalInvariantError(
                f"Database Error while fetching users. {str(e)}")

    @staticmethod
    def get_user(db: DbSession, user_id: uuid.UUID) -> UserResponseSchema:
        try:
            user: User | None = UserRepository.get_user_by_id(db, user_id)

            if not user:
                raise NotFoundException("user with a given id not found.")

            return UserResponseSchema.model_validate(user)
        except SQLAlchemyError as e:
            raise InternalInvariantError(
                f"Database Error while fetching user. {str(e)}")

    @staticmethod
    def get_current_user(db: DbSession, token: oauth_token_bearer) -> UserResponseSchema:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationErrorException()
        except jwt.InvalidTokenError:
            raise AuthenticationErrorException()
        user: User | None = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise AuthenticationErrorException()

        return UserResponseSchema.model_validate(user)

from uuid import UUID
from typing import Any
from sqlalchemy import select
from backend.account.models import User
from backend.core.db import DbSession


class UserRepository:
    @staticmethod
    def create_user(db: DbSession, serialized_data: dict[str, Any]) -> User:
        instance = User(**serialized_data)

        db.add(instance)

        db.commit()

        db.refresh(instance)

        return instance

    @staticmethod
    def get_users(db: DbSession):
        result = db.scalars(select(User))
        return result

    @staticmethod
    def get_user_by_id(db: DbSession, user_id: UUID) -> User | None:
        user: User | None = db.get(User, user_id)

        return user

    @staticmethod
    def get_user_by_email(db: DbSession, email: str):
        user: User | None = db.scalar(select(User).where(User.email == email))

        return user

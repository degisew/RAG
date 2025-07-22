from datetime import timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth.schemas import TokenSchema
from backend.auth.services import AuthService
from backend.core.db import DbSession
from backend.core.exceptions import AuthenticationErrorException
from backend.core.config import settings


router = APIRouter(prefix="/auth", tags=["Auth"])


ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES


@router.post("/token")
async def login_for_access_token(
    db: DbSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    user = AuthService.authenticate_user(
        db, form_data.username, form_data.password)

    if not user:
        raise AuthenticationErrorException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = AuthService.create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )

    obj: dict[str, str] = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    return TokenSchema.model_validate(obj)



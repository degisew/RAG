from typing import Annotated
from fastapi import Depends
from backend.account.schemas import UserResponseSchema
from backend.account.services import UserService


CurrentUser = Annotated[UserResponseSchema,
                        Depends(UserService.get_current_user)]

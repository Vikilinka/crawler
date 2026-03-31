from typing import Annotated

from fastapi import APIRouter, Depends, Security
from fastapi.responses import RedirectResponse

from apps.welcome.tools.type import Token, User
from apps.welcome.tools.user import get_token, get_current_user, get_new_user, change_password


router = APIRouter()
welcome_router = router

@router.get('/')
def root() -> RedirectResponse:
    return RedirectResponse('/docs')

@router.post('/token')
def login_for_access_token(token: Token = Depends(get_token)) -> Token:
    return token

@router.get('/whoami')
def show_current_user(current_user: Annotated[User, Security(get_current_user)]) -> User:
    return current_user

@router.post('/password')
def change_password_for_current_user(_: Annotated[None, Depends(change_password)]) -> None:
    return None

@router.post('/user')
def create_user(
        _: Annotated[User, Security(get_current_user, scopes=['admin'])],
        new_user: Annotated[User, Depends(get_new_user)]
) -> User:
    return new_user

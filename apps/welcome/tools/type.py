from typing import Any

from pydantic import BaseModel, RootModel, EmailStr, constr


class OpenAPI(RootModel[dict[str, Any]]):
    root: dict[str, Any]


class Token(RootModel[str]):
    root: str


class Email(RootModel[EmailStr]):
    root: EmailStr


class Password(RootModel[str]):
    root: constr(min_length=6)


class HashedPassword(RootModel[str]):
    root: str


class Scope(RootModel[str]):
    root: str


class User(BaseModel):
    email: Email
    scopes: list[Scope] = []


class UserWithPassword(User):
    password: Password


class UserWithHashedPassword(User):
    password: HashedPassword


class UserLogIn(BaseModel):
    email: Email
    password: Password

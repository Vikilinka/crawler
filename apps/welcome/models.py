from typing import Union

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class Welcome(SQLModel):
    __table_args__ = {'schema': 'welcome'}

    def serialize(self) -> dict:
        return self.model_dump()


class UserScopeLink(Welcome, table=True):
    user_id: Union[int, None] = Field(default=None, foreign_key='welcome.user.id', primary_key=True)
    scope_id: Union[int, None] = Field(default=None, foreign_key='welcome.scope.id', primary_key=True)


# noinspection PyTypeHints,PyUnresolvedReferences
class User(Welcome, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    email_id: int = Field(default=None, foreign_key='welcome.email.id')
    email: 'apps.welcome.models.Email' = Relationship(back_populates='user')
    password_id: int = Field(default=None, foreign_key='welcome.password.id')
    password: 'apps.welcome.models.Password' = Relationship(back_populates='user')
    scopes: list['apps.welcome.models.Scope'] = Relationship(back_populates='users', link_model=UserScopeLink)

    def serialize(self) -> dict:
        return {
            'email': self.email.email,
            'password': self.password.password,
            'scopes': [s.scope for s in self.scopes]
        }


class Email(Welcome, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    user: User = Relationship(back_populates='email')


class Password(Welcome, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    password: str
    user: User = Relationship(back_populates='password')


class Scope(Welcome, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    scope: str = Field(index=True)
    users: list[User] = Relationship(back_populates='scopes', link_model=UserScopeLink)

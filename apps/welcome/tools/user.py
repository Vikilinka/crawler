import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from bcrypt import checkpw, hashpw, gensalt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, SecurityScopes, HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPAuthorizationCredentials as HTTPAuthCred
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select

import apps.welcome.models as models
from apps.welcome.tools.type import *
from essentials.database.orm import SessionDep, get_or_create


SECRET_KEY = '7e198bff10ebafa8d890fb63e91f8f0749b95f9b4010d022a959d3a221da9bde'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 3

oauth2_scheme = HTTPBearer(scheme_name='token')
basic_scheme = HTTPBasic()


def verify_password(plain_password: Password, hashed_password: HashedPassword) -> bool:
    return checkpw(plain_password.model_dump().encode('utf-8'), hashed_password.model_dump().encode('utf-8'))

def hash_password(password: Password) -> HashedPassword:
    return HashedPassword(root=hashpw(password.model_dump().encode('utf-8'), gensalt()).decode('utf-8'))

def get_user(session: SessionDep, email: Email) -> Union[UserWithHashedPassword, None]:
    user = session.exec(select(models.User).where(models.User.email.has(email=email.model_dump()))).one_or_none()
    if user:
        return UserWithHashedPassword(**user.serialize())
    return None

def authenticate_user(session: SessionDep, email: Email, password: Password) -> Union[UserWithHashedPassword, None]:
    user = get_user(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: User, expires_delta: Union[timedelta, None] = None) -> Token:
    to_encode = data.model_dump()
    to_encode['sub'] = to_encode.pop('email')
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
        session: SessionDep,
        security_scopes: SecurityScopes,
        token: Annotated[HTTPAuthCred, Depends(oauth2_scheme)],
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = Email(root=payload.get('sub'))
        if email.model_dump() is None:
            raise credentials_exception
        scopes = payload.get('scopes', [])
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, email=email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in scopes and not 'admin' in scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not enough permissions',
                headers={'WWW-Authenticate': authenticate_value},
            )
    scopes = [Scope(root=scope) for scope in scopes]
    return User(email=email, scopes=scopes)

def get_current_user_with_base_auth(
        session: SessionDep,
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_scheme)]
) -> User:
    try:
        # noinspection PyTypeChecker
        user = authenticate_user(session, Email(root=credentials.username), Password(root=credentials.password))
    except ValidationError:
        user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )
    return user

def get_token(session: SessionDep, user: UserLogIn) -> Token:
    user = authenticate_user(session, user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data=user, expires_delta=access_token_expires
    )
    return access_token

def get_new_user(session: SessionDep, user: UserWithPassword) -> User:
    email = models.Email(email=user.email.model_dump())
    password = models.Password(password=hash_password(user.password).model_dump())
    scopes = [get_or_create(session, models.Scope, scope=scope.model_dump()) for scope in user.scopes]
    user = models.User(email=email, password=password, scopes=scopes)
    session.add(user)
    # noinspection PyBroadException
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail='User already exist')
    session.refresh(user)
    return User(**user.serialize())

def get_default_user(session: SessionDep) -> User:
    # noinspection PyTypeChecker
    email = Email(root=os.getenv('DSA_EMAIL'))
    password = Password(root=os.getenv('DSA_PASSWORD'))
    scopes = [Scope(root='admin')]
    user = authenticate_user(session, email, password)
    if not user:
        user = UserWithPassword(email=email, password=password, scopes=scopes)
        user = get_new_user(session, user)
    return user

def change_password(
        password: Password,
        current_user: Annotated[User, Security(get_current_user)],
        session: SessionDep
) -> None:
    email = current_user.email.model_dump()
    user = session.exec(select(models.User).where(models.User.email.has(email=email))).one_or_none()
    user.password.password = hash_password(password).model_dump()
    session.commit()
    session.refresh(user)

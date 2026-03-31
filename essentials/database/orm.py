import os
from contextlib import contextmanager
from typing import Annotated, Type

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

authority = f'{os.getenv('DSA_USERNAME')}:{os.getenv('DSA_PASSWORD')}'
host = os.getenv('DSA_SQL_HOST')
database = os.getenv('DSA_DATABASE')
port = 5432
sql_url = f'postgresql://{authority}@{host}:{port}/{database}'
engine = create_engine(sql_url)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> None:
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context() -> None:
    yield from get_session()

def get_or_create[T, **P](session: Session, model: Type[T], defaults: dict = None, **kwargs: P.kwargs) -> T:
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        # noinspection PyBroadException
        try:
            session.add(instance)
            session.commit()
        except Exception:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance
        else:
            return instance


SessionDep = Annotated[Session, Depends(get_session)]

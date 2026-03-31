import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.crawler.main import crawler_router
from apps.welcome.tools.docs import get_docs_router
from essentials.broadcaster.broadcast import broadcast
from essentials.database.orm import create_db_and_tables
from apps.welcome.main import welcome_router
from apps.magnetic.main import magnetic_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    await broadcast.connect()
    yield
    await broadcast.disconnect()

app = FastAPI(
    title=os.getenv('DSA_PROJNAME'),
    version='1.0.0',
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)
app.include_router(get_docs_router(app), tags=['welcome'], include_in_schema=False)
app.include_router(welcome_router, tags=['welcome'])
app.include_router(crawler_router, tags=['crawler'], prefix='/crawler')
app.include_router(magnetic_router, tags=['magnetic'], prefix='/magnetic')

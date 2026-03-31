import os

from fastapi import APIRouter, Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from apps.welcome.tools.type import OpenAPI
from apps.welcome.tools.user import get_current_user_with_base_auth, get_default_user


def get_docs_router(app: FastAPI) -> APIRouter:
    router = APIRouter(dependencies=[Depends(get_default_user), Depends(get_current_user_with_base_auth)])

    @router.get('/openapi.json')
    async def open_api() -> OpenAPI:
        return get_openapi(
            title=os.getenv('DSA_PROJNAME'),
            version='1.0.0',
            routes=app.routes
        )

    @router.get('/docs')
    async def swagger() -> HTMLResponse:
        return get_swagger_ui_html(
            title=os.getenv('DSA_PROJNAME'),
            openapi_url='/openapi.json',
            swagger_favicon_url='/favicon.ico'
        )

    @router.get('/redoc')
    async def redoc() -> HTMLResponse:
        return get_redoc_html(
            title=os.getenv('DSA_PROJNAME'),
            openapi_url='/openapi.json'
        )

    return router

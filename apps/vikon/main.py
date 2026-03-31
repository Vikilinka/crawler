from typing import Annotated

from fastapi import APIRouter, Security
from pydantic import UUID4
from fastapi import WebSocket

from apps.vikon.core.tools.router.type.local import Programs
from apps.vikon.tasks import trace, get_programs
from apps.vikon.core.tools.router.task import VikonStatus
from apps.vikon.tools.task import get_status, get_result, broadcast_status
from apps.welcome.models import User
from apps.welcome.tools.user import get_current_user


router = APIRouter()
vikon_router = router

@router.post('/trace/')
def run_trace(programs: Programs) -> UUID4:
    trace_id = trace.delay(programs.model_dump())
    trace_id = str(trace_id)
    return trace_id

@router.get('/trace/status/{trace_id}')
def show_trace_status(trace_id: UUID4) -> VikonStatus:
    """WebSocket compatible"""
    return get_status(trace_id, VikonStatus)

@router.websocket('/trace/status/{trace_id}')
async def show_trace_status_ws(websocket: WebSocket, trace_id: UUID4) -> None:
    await broadcast_status(websocket, trace_id, VikonStatus)


@router.post('/get_programs/')
def run_get_programs(_: Annotated[User, Security(get_current_user, scopes=['vikon'])]) -> UUID4:
    get_programs_id = get_programs.delay()
    get_programs_id = str(get_programs_id)
    return get_programs_id

@router.get('/get_programs/status/{get_programs_id}')
def show_get_programs_status(get_programs_id: UUID4) -> VikonStatus:
    """WebSocket compatible"""
    return get_status(get_programs_id, VikonStatus)

@router.websocket('/get_programs/status/{get_programs_id}')
async def show_get_programs_status_ws(websocket: WebSocket, get_programs_id: UUID4) -> None:
    await broadcast_status(websocket, get_programs_id, VikonStatus)

@router.get('/get_programs/result/{get_programs_id}')
def show_get_programs_result(trace_id: UUID4) -> Programs:
    return get_result(trace_id, Programs)

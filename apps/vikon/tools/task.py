import json
from asyncio import sleep
from typing import Type, Union

from celery import Task
from pydantic import Json, TypeAdapter
from fastapi import WebSocket

from apps.vikon.core.tools.router.type.local import Status
from essentials.broadcaster.broadcast import broadcast
from essentials.celery.worker import app


class Retry(Task):
    autoretry_for = (Exception,)
    default_retry_delay = 1
    max_retries = 5
    retry_backoff = True
    retry_jitter = True


def get_status[T: Status](task_id: int, status_type: Type[T]) -> T:
    status = status_type()
    # noinspection PyBroadException
    try:
        async_result = app.AsyncResult(str(task_id))
        state = async_result.state.lower()
        info = async_result.info or {}
        status = status.model_copy(update=info.get('status', {}))
        status.state = state
    except Exception:
        status.state = 'error'
    return status

def get_status_json(task_id: int, status_type: Type[Status]) -> Json:
    status = get_status(task_id, status_type)
    return json.dumps(status.model_dump())

async def broadcast_status(websocket: WebSocket, task_id: int, status_type: Type[Status]) -> None:
    await websocket.accept()
    await websocket.send_text(get_status_json(task_id, status_type))
    async with broadcast.subscribe(channel=f'task_{task_id}') as subscriber:
        async for event in subscriber:
            match event.message:
                case 'update_state':
                    await websocket.send_text(get_status_json(task_id, status_type))
                case 'completion':
                    break
    while True:
        await sleep(0.1)
        status = dict(get_status(task_id, status_type))
        await websocket.send_text(get_status_json(task_id, status_type))
        if status['state'] != 'progress':
            break

def get_result[T](task_id: int, result_type: Type[T]) -> Union[T, None]:
    async_result = app.AsyncResult(str(task_id))
    if async_result.ready():
        result = async_result.result
        result = result.get('result', {})
        result = TypeAdapter(result_type).validate_python(result)
    else:
        result = None
    return result

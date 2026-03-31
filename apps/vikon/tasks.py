from celery import Task

from apps.vikon.core.router.VikonRouter import VikonRouter
from apps.vikon.core.tools.router.type.local import Result, Programs, Trace
from apps.vikon.tools.task import Retry
from essentials.celery.worker import app


@app.task(bind=True)
def trace(task: Task, programs: Programs = ()) -> Result[Trace]:
    vikon_router = VikonRouter(task)
    result = vikon_router.trace(programs)
    result = result.model_dump()
    return result

@app.task(bind=True)
def get_programs(task: Task) -> Result[Programs]:
    vikon_router = VikonRouter(task)
    result = vikon_router.get_programs()
    result = result.model_dump()
    return result

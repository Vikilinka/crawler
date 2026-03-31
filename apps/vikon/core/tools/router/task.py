import asyncio

from celery import Task

from apps.vikon.core.tools.router.type.local import Meta as TypeMeta
from apps.vikon.core.tools.router.type.local import VikonStatus, Result
from essentials.broadcaster.broadcast import broadcast


class Meta:
    def __init__(self, task: Task):
        self.task = task
        self.task_id = self.task.request.id
        self.cache_id = self.task_id
        self.status = VikonStatus()
        self._update_state()

    def set_value(self, value_name: str, amount: int) -> None:
        setattr(self.status, value_name, amount)
        self._update_state()

    def inc_value(self, value_name: str) -> None:
        amount = getattr(self.status, value_name)
        amount += 1
        setattr(self.status, value_name, amount)
        self._update_state()

    def dec_value(self, value_name: str) -> None:
        amount = getattr(self.status, value_name)
        amount -= 1
        setattr(self.status, value_name, amount)
        self._update_state()

    def get_status(self) -> VikonStatus:
        return self.status

    def _update_state(self) -> None:
        result = Result[TypeMeta](status=self.status, result=None)
        self.task.update_state(state='PROGRESS', meta=result.model_dump())
        asyncio.get_event_loop().run_until_complete(self._broadcast('update_state'))

    async def _broadcast(self, message: str) -> None:
        await broadcast.publish(f'task_{self.task_id}', message)

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self._broadcast('completion'))

import os
from contextlib import asynccontextmanager

from broadcaster import Broadcast as BaseBroadcast


authority = f':{os.getenv('DSA_PASSWORD')}'
host = os.getenv('DSA_NOSQL_HOST')
database = '1'
port = 6379
nosql_url = f'redis://{authority}@{host}:{port}/{database}'
broadcast = BaseBroadcast(nosql_url)

# class Broadcast:
#     def __init__(self):
#         self.base_broadcast = BaseBroadcast(f'redis://:{os.getenv('DSA_PASSWORD')}@redis:6379/1')
#
#     async def publish(self, task_id, message):
#         await self.base_broadcast.publish(f'task_{task_id}', message)
#
#     @asynccontextmanager
#     async def subscribe(self, task_id):
#         async with self.base_broadcast.subscribe(channel=f'task_{task_id}') as subscriber:
#             yield subscriber

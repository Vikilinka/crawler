import os

imports = ['apps']
broker_url = f'redis://:{os.getenv('DSA_PASSWORD')}@redis:6379/0'
result_backend = f'redis://:{os.getenv('DSA_PASSWORD')}@redis:6379/0'
task_acks_late = True
task_reject_on_worker_lost = True

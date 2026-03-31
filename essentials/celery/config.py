import os
from celery.schedules import crontab

imports = ['apps']
broker_url = f'redis://:{os.getenv('DSA_PASSWORD')}@redis:6379/0'
result_backend = f'redis://:{os.getenv('DSA_PASSWORD')}@redis:6379/0'
task_acks_late = True
task_reject_on_worker_lost = True

# Расписание для Celery Beat
beat_schedule = {
    # Запуск краулинга всех доменов раз в час
    'crawl-all-domains-hourly': {
        'task': 'apps.crawler.tasks.crawl_all_domains_task',
        'schedule': crontab(minute=0),  # Каждый час в 0 минут
        'options': {'queue': 'default'}
    },
}

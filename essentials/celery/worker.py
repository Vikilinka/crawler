from celery import Celery
from celery.schedules import crontab


app = Celery('tasks')
app.config_from_object('essentials.celery.config')

# Расписание для Celery Beat
app.conf.beat_schedule = {
    # Запуск краулинга всех доменов каждый час в 0 минут
    'crawl-all-domains-hourly': {
        'task': 'apps.crawler.tasks.crawl_all_domains_task',
        'schedule': crontab(minute=0),  # Каждый час в 0 минут
    },
}

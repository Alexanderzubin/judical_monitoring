import logging

from celery import Celery, signals
from celery.schedules import crontab

from app.logging_config import setup_logging
from app.settings import settings


app = Celery(
    'judicial_monitoring_bot',
    broker=str(settings.celery.broker_url),
    backend=str(settings.celery.backend_url),
)

app.conf.update(
    content_encoding='utf-8',
    accept_content=['application/json'],
    redbeat_redis_url=str(settings.celery.redbeat_redis_url),
    beat_scheduler='redbeat.RedBeatScheduler',
    task_serializer='json',
    result_serializer='json',
)

app.autodiscover_tasks(['app.tasks'])


app.conf.beat_schedule = {
    'update_all_cases': {
        'task': 'app.tasks.scheduler.async_update_all_cases',
        'schedule': crontab(hour='*', minute='*'),  # every day at 00:00
    },
}


@signals.after_setup_logger.connect
def on_after_setup_logger(**kwargs):
    setup_logging()
    logger = logging.getLogger('celery')
    logger.propagate = True
    logger = logging.getLogger('celery.app.trace')
    logger.propagate = True

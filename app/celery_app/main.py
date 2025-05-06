from celery import Celery
from celery.schedules import crontab


app = Celery(
    'tasks',
    broker='postgresql://postgres:.....@smilingly-amicable-courser.data-1.euc1.tembo.io:5432/postgres',
    backend='postgresql://postgres:.....@smilingly-amicable-courser.data-1.euc1.tembo.io:5432/postgres'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'check-all-cases': {
        'task': 'app.tasks.check_all_cases_task',
        'schedule': crontab(hour=23, minute=0),  # Каждый день в 23:00
    },
}



#СЮДА ИМПОРТИРОВАТЬ ВСЕ ТАСКИ ИЗ МОДУЛЯ tasks
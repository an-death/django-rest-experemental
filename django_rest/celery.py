from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from django_rest.settings import BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest.settings')
app = Celery('django_rest', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    include=['django_rest.tasks']
)
app.conf.beat_schedule = {
    'check_out_vacancies_every_day': {
        'task': 'tasks.check_out_vacancies',
        'schedule': crontab(),
    },
}
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()

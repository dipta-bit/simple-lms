import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


app = Celery('lms_celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'amqp://guest:guest@rabbitmq:5672//'

app.autodiscover_tasks()
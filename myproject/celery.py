import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

app = Celery("myproject")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-orders-every-5-seconds': {
        'task': 'food.tasks.check_orders_status',
        'schedule': 5.0,  # каждые 5 секунд
    },
}
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE','library.settings')
app = Celery('library')
app.config_from_object('django.conf:settings', namespace='CELERY')

from library_management.tasks import add
from datetime import timedelta
app.conf.beat_schedule = {
    'print-every-10-seconds':{
        'task':'library_management.tasks.add',
        'schedule':timedelta(seconds=10)
    }
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
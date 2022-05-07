from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from csm.dataprocessing.lib.config import Configuration

cfg = Configuration()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "processing_spreadsheet": {
        "task": "csm.dataprocessing.spreadsheet.processing_spreadsheet",
        "schedule": crontab(hour=cfg.get_time(start=True)[0],
                            minute=cfg.get_time(start=True)[1],
                            day_of_month=cfg.get_day_of_month(start=True, end=True)),
    },
}
app.conf.timezone = 'Europe/Prague'

app.autodiscover_tasks()

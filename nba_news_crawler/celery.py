from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set default settings of Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_news_crawler.settings')

app = Celery('nba_news_crawler')

# Use settings to config Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

from __future__ import absolute_import, unicode_literals
import logging
import os
from celery import Celery
from django.conf import settings


logger = logging.getLogger("scheduler")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeApp.settings")

app = Celery("recipeApp")
app.conf.enable_utc = False
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {self.request!r}")


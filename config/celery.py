from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Установите модуль настроек Django по умолчанию для 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("project_name")

# Используйте строку настроек Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживайте задачи в приложениях Django
app.autodiscover_tasks()

import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
app = Celery('Ecommerce')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# django-celery backend
if 'djcelery' in settings.INSTALLED_APPS:
    # For the database backend you must use:
    app.conf.update(
        CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    )
    # For the cache backend you can use:
    # app.conf.update(
    #     CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    # )

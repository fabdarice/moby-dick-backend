import os

from celery import Celery

db_uri = os.environ.get('DATABASE_URI')
celery = Celery('moby_tasks', broker=f'db+{db_uri}')

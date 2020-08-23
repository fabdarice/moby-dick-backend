import os

from celery import Celery

imports = 'app.tasks.hodler'

broker_url = os.environ.get('REDIS_URI')
backend_url = os.environ.get('REDIS_URI')

task_acks_late = True
task_routes = {
    'app.tasks.hodler.create_token_hodlers_task': {'queue': 'main'},
}

celery = Celery(broker=broker_url, backend=backend_url)
celery.config_from_object('app.celeryconfig')

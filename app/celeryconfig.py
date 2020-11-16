import os

from celery import Celery

imports = ('app.tasks.hodler', 'app.tasks.blockchain')

broker_url = os.environ.get('REDIS_URL')
backend_url = os.environ.get('REDIS_URL')
block_frequency = os.environ.get('BLOCK_FREQUENCY', 30)

task_acks_late = True
task_routes = {
    'app.tasks.hodler.blockchain_events_sync_one_contract': {'queue': 'main'},
    'app.tasks.blockchain.blockchain_events_sync_all_contracts': {'queue': 'main'},
}

beat_schedule = {
    'main': {
        'task': 'app.tasks.blockchain.blockchain_events_sync_all_contracts',
        'schedule': block_frequency,
    },
}


celery = Celery(broker=broker_url, backend=backend_url)
celery.config_from_object('app.celeryconfig')

import time
import os
from typing import Dict

from flask import Flask
from contextlib import contextmanager
from celery.utils.log import get_task_logger
from flask_caching import Cache

from app.celeryconfig import celery
from app.services.blockchain import BlockchainService
from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token

logger = get_task_logger(__name__)

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
LOCK_EXPIRE = 60  # Lock expires in 1 minute

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


@contextmanager
def memcache_lock(lock_id):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@celery.task
def create_token_hodlers_task(token_dict: Dict):
    with memcache_lock('create_token_hodlers') as acquired:
        if acquired:
            token = Token.from_dict(token_dict)
            if ETHERSCAN_API_KEY is None:
                raise Exception('INFURA_WS_URI or ETHERSCAN_API_KEY is not set')
            hodler_svc = HodlerService()
            token_svc = TokenService()

            blockchain_svc = BlockchainService(token_svc, hodler_svc, ETHERSCAN_API_KEY)
            blockchain_svc.create_all_tokens_hodlers(token)

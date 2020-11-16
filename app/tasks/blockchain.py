import time
import os
from typing import Any, Dict
from dataclasses import asdict

from flask_caching import Cache
from flask import Flask
from contextlib import contextmanager

from app.celeryconfig import celery
from app.services.token import TokenService
from app.services.blockchain import BlockchainService
from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token
from wsgi import app

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')
if ETHERSCAN_API_KEY is None:
    raise Exception('ETHERSCAN_API_KEY is not set')

LOCK_EXPIRE = 60  # Lock expires in 1 minute

cache = Cache(app, config={'CACHE_TYPE': 'redis'})


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    print(f"FAB {status}")
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@celery.task(bind=True)
def blockchain_events_sync_one_contract(self, token_dict: Dict[str, Any], max_retries=None):
    """This task will sync the blockchain for all events for a single contract
    and update the TOP hodlers
    """
    with memcache_lock(token_dict['name'], self.app.oid) as acquired:
        if acquired:
            token = Token.from_dict(token_dict)
            hodler_svc = HodlerService()
            token_svc = TokenService()
            blockchain_svc = BlockchainService(token_svc, hodler_svc, ETHERSCAN_API_KEY)
            token = blockchain_svc.update_hodlers(token)
            if not token.synced:
                blockchain_events_sync_one_contract.apply_async(args=[asdict(token)])


@celery.task
def blockchain_events_sync_all_contracts(max_retries=None):
    """This task will sync the blockchain for each Token contract we support
    and update the top hodlers balance
    """
    token_svc = TokenService()
    tokens = token_svc.get_tokens()
    synced_tokens = [token for token in tokens if token.synced]
    for synced_token in synced_tokens:
        blockchain_events_sync_one_contract.apply(args=[asdict(synced_token)])

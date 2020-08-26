import os
from typing import Any, Dict

from app.celeryconfig import celery
from app.controllers.token import TokenController
from app.services.blockchain import BlockchainService
from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token

WS_URI = os.environ.get('INFURA_WS_URI')
ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')


@celery.task
def blockchain_events_sync_one_contract(token_dict: Dict[str, Any], max_retries=None):
    """This task will sync the blockchain for all events for a single contract
    and update the TOP hodlers
    """
    token = Token.from_dict(token_dict)
    if WS_URI is None or ETHERSCAN_API_KEY is None:
        raise Exception('INFURA_WS_URI or ETHERSCAN_API_KEY is not set')
    hodler_svc = HodlerService()
    token_svc = TokenService()
    blockchain_svc = BlockchainService(token_svc, hodler_svc, WS_URI, ETHERSCAN_API_KEY)
    blockchain_svc.update_hodlers(token)


@celery.task
def blockchain_events_sync_all_contracts(max_retries=None):
    """This task will sync the blockchain for each Token contract we support
    and update the top hodlers balance
    """
    token_ctl = TokenController()
    tokens = token_ctl.get_tokens()
    synced_tokens = [token for token in tokens if token.synced]
    for synced_token in synced_tokens:
        blockchain_events_sync_one_contract.apply_async(synced_token.to_dict())

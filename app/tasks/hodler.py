import os
from typing import Dict

from celery.utils.log import get_task_logger

from app.celeryconfig import celery
from app.services.blockchain import BlockchainService
from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token

logger = get_task_logger(__name__)

ETHERSCAN_API_KEY = os.environ.get('ETHERSCAN_API_KEY')


@celery.task
def create_token_hodlers_task(token_dict: Dict):
    token = Token.from_dict(token_dict)
    if ETHERSCAN_API_KEY is None:
        raise Exception('INFURA_WS_URI or ETHERSCAN_API_KEY is not set')
    hodler_svc = HodlerService()
    token_svc = TokenService()

    blockchain_svc = BlockchainService(token_svc, hodler_svc, ETHERSCAN_API_KEY)
    blockchain_svc.create_all_tokens_hodlers(token)

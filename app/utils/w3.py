import logging
import os

from web3 import Web3

from app.utils.borg import Borg

GETH_HTTP_URI = os.environ.get('GETH_HTTP_URI', None)
GETH_WS_URI = os.environ.get('GETH_WS_URI', None)


class Web3ProviderBorg(Borg):
    def __init__(self) -> None:
        super().__init__()

    def use_connection(self):
        if hasattr(self, 'w3') and self.w3.isConnected():
            return self.w3
        logging.info('No Connection.. Opening a new web3 websocket connection')
        if GETH_WS_URI:
            self.w3 = Web3(Web3.WebsocketProvider(GETH_WS_URI))
            return self.w3
        if GETH_HTTP_URI:
            self.w3 = Web3(Web3.HTTPProvider(GETH_HTTP_URI))
            return self.w3
        raise Exception('Geth WS/HTTP URI is not defined in configuration.')


Web3ProviderSession = Web3ProviderBorg()

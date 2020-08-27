import logging
import os

from web3 import Web3

from app.utils.borg import Borg

INFURA_WS_URI = os.environ.get('INFURA_WS_URI')


class Web3ProviderBorg(Borg):
    def __init__(self) -> None:
        super().__init__()

    def use_connection(self):
        if hasattr(self, 'w3') and self.w3.isConnected():
            return self.w3
        logging.info('No Connection.. Opening a new web3 websocket connection')
        self.w3 = Web3(Web3.WebsocketProvider(INFURA_WS_URI))
        return self.w3


Web3ProviderSession = Web3ProviderBorg()

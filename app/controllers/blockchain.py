import json
import logging
import os

import requests
from web3 import Web3
from web3.eth import Contract

from app.models.token import Token

ETHERSCAN_API = 'https://etherscan.io/'
BLOCK_THRESHOLD = os.environ.get('BLOCK_THRESHOLD', 1000)


class BlockchainController:
    def __init__(self) -> None:
        ws_uri = os.environ.get('INFURA_WS_URI')
        self.etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')
        if ws_uri is None or self.etherscan_api_key is None:
            logging.error('INFURAi_WS_URI or ETHERSCAN_API_KEY is not set')
        self.web3 = Web3(Web3.WebsocketProvider(ws_uri))
        if not self.web3.isConnected():
            logging.error(f'Web3 is not Connected.')

    def fetch_events_from_creation(self, token: Token) -> None:
        """Fetch all events from Creation"""
        contract = self._init_contract(self.web3.toChecksumAddress(token.contract_address))
        last_block = self._get_latest_block_number()
        while token.last_block != last_block:
            transfer_filter = contract.events.Transfer.createFilter(
                fromBlock=latest_block, toBlock=latest_block + BLOCK_THRESHOLD
            )
            current_block = int(latest_block)
            event_list = transfer_filter.get_all_entries()
            for event in event_list:
                print(event)
                # allInfo = my_contract.functions.allInfoFor(event["args"]["owner"]).call()
                # balance = f'UserBalance: {int(w3.fromWei(allInfo[2], "ether")):,} | UserFrozen: {int(w3.fromWei(allInfo[3], "ether")):,}'


    def _get_abi(self, contract_address: str) -> str:
        """Fetch a contract ABI"""
        url = f'{ETHERSCAN_API}?module=contract&action=getabi&address={contract_address}&apikey={self.etherscan_api_key}'
        resp = requests.get(url)
        json_resp = json.loads(resp.text)
        contract_abi = json_resp['result']
        return contract_abi

    def _init_contract(self, contract_address: str) -> Contract:
        """Initialize a web3.eth.Contract object"""
        abi = self._get_abi(contract_address)
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        return contract

    def _get_latest_block_number(self) -> int:
        url = f'{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={self.etherscan_api_key}'
        resp = requests.get(url)
        hex_block = json.loads(resp.text)["result"]
        return int(hex_block, 16)

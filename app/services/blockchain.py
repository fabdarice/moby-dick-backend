import json
import logging
import os
import time
from collections import defaultdict
from typing import Dict

import requests
from web3 import Web3
from web3.eth import Contract

from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token

ETHERSCAN_API = 'https://api.etherscan.io/api'
BLOCK_THRESHOLD = int(os.environ.get('BLOCK_THRESHOLD', 500))


class BlockchainService:
    def __init__(
        self,
        token_svc: TokenService,
        hodler_svc: HodlerService,
        infura_ws: str,
        etherscan_api_key: str,
    ) -> None:
        self.hodler_svc = hodler_svc
        self.token_svc = token_svc
        self.web3 = Web3(Web3.WebsocketProvider(infura_ws))
        self.infura_ws = infura_ws
        if not self.web3.isConnected():
            logging.error(f'Web3 is not Connected.')
        self.etherscan_api_key = etherscan_api_key

    def connection(self) -> None:
        """Connection to web3 if connection is closed"""
        if self.web3.isConnected():
            return
        logging.info('Connecting to web3..')
        self.web3 = Web3(Web3.WebsocketProvider(self.infura_ws))

    def create_all_tokens_hodlers(self, token: Token) -> None:
        """Fetch all events from Creation and calculate token hodlers"""
        contract = self._init_contract(self.web3.toChecksumAddress(token.contract_address))

        hodlers = defaultdict(dict)
        # hodlers = self.hodler_svc.find_by_token_name(token.name)
        # hodlers_by_address = {hodler.address: hodler for hodler in hodlers}
        eth_last_block = self._get_latest_block_number()
        token_last_block = token.block_creation
        counter = 0
        while token_last_block != eth_last_block:
            try:
                to_block = min(token_last_block + BLOCK_THRESHOLD, eth_last_block)
                transfer_filter = contract.events.Transfer.createFilter(
                    fromBlock=token_last_block + 1, toBlock=to_block
                )
                event_list = transfer_filter.get_all_entries()
                for event in event_list:
                    self._parse_event(hodlers, event, token.name)

                token_last_block = min(eth_last_block, to_block)
                time.sleep(0.05)
                token.last_block = token_last_block
                counter += 1
                if counter % 10 == 0:
                    self.token_svc.update_token(token)
                    print(f'{token.last_block}/{eth_last_block}')
            except Exception as e:
                logging.error(f'Web3 connection failed {str(e)}. Reconnecting..')
                self.connection()
                continue
        filter_empty_hodlers = []
        for hodler_addr, hodler in hodlers.items():
            if hodler['amount'] < 100000000000000:
                filter_empty_hodlers.append(hodler_addr)
            hodler['amount'] = str(hodler['amount']).zfill(32)

        for hodler_addr in filter_empty_hodlers:
            del hodlers[hodler_addr]
        self.hodler_svc.save_hodlers(list(hodlers.values()))
        token.synced = True
        self.token_svc.update_token(token)

    def _parse_event(self, hodlers: Dict[str, Dict], event, token_name: str):
        """Parse Transfer Event and update amount for seller/buyer"""
        seller = event['args']['from']
        buyer = event['args']['to']
        amount = event['args']['tokens']
        for hodler in [seller, buyer]:
            if hodler not in hodlers:
                hodlers[hodler] = {
                    'amount': 0,
                    'number_transactions': 0,
                    'token_name': token_name,
                    'address': hodler,
                }
        hodlers[seller]['amount'] -= amount
        hodlers[seller]['number_transactions'] += 1
        hodlers[buyer]['amount'] += amount
        hodlers[buyer]['number_transactions'] += 1

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

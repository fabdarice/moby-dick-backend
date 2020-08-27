import json
import os
import time
from collections import defaultdict
from typing import Dict

import requests
from celery.utils.log import get_task_logger
from web3.eth import Contract
from websockets.exceptions import ConnectionClosed

from app.services.hodler import HodlerService
from app.services.token import TokenService
from app.ttypes.token import Token
from app.utils.w3 import Web3ProviderSession

ETHERSCAN_API = 'https://api.etherscan.io/api'
INFURA_WS_URI = os.environ.get('INFURA_WS_URI')
INFURA_HUY = 'wss://mainnet.infura.io/ws/v3/90409d9baead4e1c9cd9a54cb8774216'

BLOCK_THRESHOLD = int(os.environ.get('BLOCK_THRESHOLD', 100))
logger = get_task_logger(__name__)


class BlockchainService:
    def __init__(
        self, token_svc: TokenService, hodler_svc: HodlerService, etherscan_api_key: str,
    ) -> None:
        self.hodler_svc = hodler_svc
        self.token_svc = token_svc
        self.etherscan_api_key = etherscan_api_key
        self.w3 = Web3ProviderSession.use_connection()

    def ensure_web3_connection(self) -> None:
        """Connection to web3 if connection is closed"""
        if self.w3.isConnected():
            return
        self.w3 = Web3ProviderSession.use_connection()

    def create_all_tokens_hodlers(self, token: Token) -> None:
        """Fetch all events from Creation and calculate token hodlers"""
        self.ensure_web3_connection()
        contract = self.init_contract(self.w3.toChecksumAddress(token.contract_address))
        hodlers = defaultdict(dict)
        eth_last_block = self._get_latest_block_number()
        token_last_block = token.block_creation
        counter = 0
        max_retry = 10
        while token_last_block != eth_last_block:
            try:
                to_block = min(token_last_block + BLOCK_THRESHOLD, eth_last_block)
                transfer_filter = contract.events.Transfer.createFilter(
                    fromBlock=token_last_block + 1, toBlock=to_block
                )
                event_list = transfer_filter.get_all_entries()
                for event in event_list:
                    self._parse_event(hodlers, event, token)

                token_last_block = min(eth_last_block, to_block)
                time.sleep(0.5)
                token.last_block = token_last_block
                counter += 1
                eth_last_block = self._get_latest_block_number()
                if counter % 10 == 0:
                    self.token_svc.update_token(token)
                    print(f'[{token.name}] Processing blocks {token.last_block}/{eth_last_block} ..')
            except ConnectionClosed as e:
                max_retry -= 1
                logger.error(f'Web3 connection failed {str(e)}. Reconnecting..')
                if max_retry > 0:
                    self.ensure_web3_connection()
                    continue
        filter_empty_hodlers = []
        for hodler_addr, hodler in hodlers.items():
            if hodler['amount'] < (token.decimal * 10) / 5:
                filter_empty_hodlers.append(hodler_addr)
            hodler['amount'] = str(hodler['amount']).zfill(32)

        for hodler_addr in filter_empty_hodlers:
            del hodlers[hodler_addr]
        if hodlers:
            self.hodler_svc.save_hodlers(list(hodlers.values()))
        token.synced = True
        self.token_svc.update_token(token)
        print(f'Top Hodlers for Token {token.name} has completed!')

    def _parse_event(self, hodlers: Dict[str, Dict], event, token: Token):
        """Parse Transfer Event and update amount for seller/buyer"""
        amount_keyword = 'tokens' if 'tokens' in event['args'] else 'value'
        seller = event['args']['from'].lower()
        buyer = event['args']['to'].lower()
        amount = event['args'][amount_keyword]
        for hodler in [seller, buyer]:
            if (
                hodler not in hodlers
                and hodler != token.contract_address.lower()
                and hodler != '0x0000000000000000000000000000000000000000'
                and hodler != token.uniswap_address.lower()
            ):
                hodlers[hodler] = {
                    'amount': 0,
                    'number_transactions': 0,
                    'token_name': token.name,
                    'address': hodler,
                    'last_transaction': '0',
                }
        if seller in hodlers:
            hodlers[seller]['amount'] -= amount
            hodlers[seller]['number_transactions'] += 1
            hodlers[seller]['last_transaction'] = f'-{amount}'
        if buyer in hodlers:
            hodlers[buyer]['amount'] += amount
            hodlers[buyer]['number_transactions'] += 1
            hodlers[buyer]['last_transaction'] = f'+{amount}'

    def _get_abi(self, contract_address: str) -> str:
        """Fetch a contract ABI"""
        url = f'{ETHERSCAN_API}?module=contract&action=getabi&address={contract_address}&apikey={self.etherscan_api_key}'
        resp = requests.get(url)
        json_resp = json.loads(resp.text)
        contract_abi = json_resp['result']
        return contract_abi

    def init_contract(self, contract_address: str) -> Contract:
        """Initialize a web3.eth.Contract object"""
        abi = self._get_abi(contract_address)
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        return contract

    def _get_latest_block_number(self) -> int:
        url = f'{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={self.etherscan_api_key}'
        resp = requests.get(url)
        hex_block = json.loads(resp.text)["result"]
        return int(hex_block, 16)

    def update_hodlers(self, token: Token) -> None:
        """Sync the blockchain for Transfer events and update the top hodlers"""
        self.ensure_web3_connection()
        eth_last_block = self._get_latest_block_number()
        contract = self.init_contract(self.w3.toChecksumAddress(token.contract_address))
        event_hodlers = defaultdict(dict)
        to_block = min(token.last_block + BLOCK_THRESHOLD, eth_last_block)
        if token.last_block < eth_last_block:
            transfer_filter = contract.events.Transfer.createFilter(
                fromBlock=token.last_block + 1, toBlock=to_block
            )
            event_list = transfer_filter.get_all_entries()
            for event in event_list:
                self._parse_event(event_hodlers, event, token)

        if event_hodlers:
            self.hodler_svc.update_hodlers(event_hodlers, token)
        token.last_block = to_block
        self.token_svc.update_token(token)

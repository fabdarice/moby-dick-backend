from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Token:
    name: str
    contract_address: str
    uniswap_address: str
    events: Dict[str, Any]
    decimal: int
    total_supply: int
    synced: bool
    last_block: str
    block_creation: str

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'contract_address': self.contract_address,
            'uniswap_address': self.uniswap_address,
            'events': self.events,
            'decimal': self.decimal,
            'total_supply': self.total_supply,
            'synced': self.synced,
            'last_block': self.last_block,
            'block_creation': self.block_creation,
        }

    @classmethod
    def from_dict(cls, token_dict) -> 'Token':
        return cls(
            name=token_dict['name'],
            contract_address=token_dict['contract_address'],
            uniswap_address=token_dict['uniswap_address'],
            events=token_dict['events'],
            decimal=token_dict['decimal'],
            synced=token_dict['synced'],
            total_supply=token_dict['total_supply'],
            last_block=token_dict['last_block'],
            block_creation=token_dict['block_creation'],
        )

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Token:
    name: str
    contract_address: str
    uniswap_address: str
    events: Dict[str, Any]
    synced: bool
    last_block: str
    block_creation: str

    def to_dict(self) -> Dict:
        asdict(self)

    @classmethod
    def from_dict(cls, token_dict) -> 'Token':
        return cls(
            name=token_dict['name'],
            contract_address=token_dict['contract_address'],
            uniswap_address=token_dict['uniswap_address'],
            events=token_dict['events'],
            synced=token_dict['synced'],
            last_block=token_dict['last_block'],
            block_creation=token_dict['block_creation'],
        )

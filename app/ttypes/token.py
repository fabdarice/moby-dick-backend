from dataclasses import dataclass
from typing import Dict


@dataclass
class Token:
    name: str
    contract_address: str
    uniswap_address: str
    events: str
    decimal: int
    total_supply: int
    synced: bool
    last_block: str
    block_creation: str
    watchlist_addresses: str
    logo_url: str
    twitter_url: str
    telegram_url: str
    website_url: str
    coingecko_url: str

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
            'watchlist_addresses': self.watchlist_addresses,
            'logo_url': self.logo_url,
            'twitter_url': self.twitter_url,
            'telegram_url': self.telegram_url,
            'website_url': self.website_url,
            'coingecko_url': self.coingecko_url,
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
            watchlist_addresses=token_dict['watchlist_addresses'],
            logo_url=token_dict['logo_url'],
            twitter_url=token_dict['twitter_url'],
            telegram_url=token_dict['telegram_url'],
            website_url=token_dict['website_url'],
            coingecko_url=token_dict['coingecko_url'],
        )

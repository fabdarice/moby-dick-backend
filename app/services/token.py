import logging
from dataclasses import asdict
from typing import Any, Dict, List

from app.models.token import TokenModel
from app.ttypes.token import Token
from app.utils.session import SessionManager


class TokenService:
    def __init__(self) -> None:
        pass

    def create_token(self, payload: Dict[str, Any]) -> Token:
        """Create Token in the database and then fetch all events since creation"""
        token = TokenModel(
            name=payload['name'].upper(),
            contract_address=payload['contract_address'].lower(),
            uniswap_address=payload['uniswap_address'].lower(),
            events=payload['events'],
            decimal=int(payload['decimal']),
            total_supply=payload['total_supply'],
            block_creation=int(payload['block_creation']),
            last_block=int(payload['block_creation']),
            synced=False,
        )

        with SessionManager.session() as session:
            session.add(token)

        return Token(
            name=token.name,
            contract_address=token.contract_address,
            uniswap_address=token.uniswap_address,
            events=token.events,
            decimal=token.decimal,
            total_supply=token.total_supply,
            synced=token.synced,
            last_block=token.last_block,
            block_creation=token.block_creation,
        )

    def get_token_by_name(self, name: str) -> Token:
        """Retrieve a Token row by its name"""
        with SessionManager.session() as session:
            token = session.query(TokenModel).filter(name=name).one()

            if not token:
                logging.error(f'Token `{name}` not found.')
        return token

    def update_token(self, token: Token) -> None:
        """Update token in database"""
        with SessionManager.session() as session:
            row = session.query(TokenModel).filter_by(name=token.name)
            row.update(asdict(token))

    def get_tokens(self) -> List[Token]:
        with SessionManager.session() as session:
            rows = session.query(TokenModel).all()

        return [
            Token(
                name=row.name,
                contract_address=row.contract_address,
                uniswap_address=row.uniswap_address,
                events=row.events,
                synced=row.synced,
                last_block=row.last_block,
                block_creation=row.block_creation,
            )
            for row in rows
        ]

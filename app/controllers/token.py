from typing import Any, Dict

from app.models.token import Token
from app.utils.session import SessionManager


class TokenController:
    def __init__(self) -> None:
        pass

    def create_token(self, payload: Dict[str, Any]) -> None:
        token = Token(
            name=payload['name'],
            contract_address=payload['contract_address'],
            uniswap_address=payload['uniswap_address'],
            events=payload['events'],
            block_creation=payload['block_creation'],
        )

        with SessionManager.session() as session:
            session.add(token)

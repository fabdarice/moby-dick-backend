from dataclasses import asdict
from typing import Any, Dict, List

from app.services.token import TokenService
from app.tasks.blockchain import blockchain_events_sync_one_contract
from app.ttypes.token import Token


class TokenController:
    def __init__(self) -> None:
        self.token_svc = TokenService()

    def create_token(self, payload: Dict[str, Any]) -> None:
        """Create Token in the database and then fetch all events since creation"""
        token = self.token_svc.create_token(payload)
        blockchain_events_sync_one_contract.apply_async(args=[asdict(token)])

    def get_token_by_name(self, name: str) -> Token:
        """Retrieve a Token row by its name"""
        return self.token_svc.get_token_by_name(name)

    def get_tokens(self) -> List[Token]:
        return self.token_svc.get_tokens()

    def edit_token(self, payload: Dict[str, Any]) -> None:
        self.token_svc.update_token_dict(payload)

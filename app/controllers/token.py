from dataclasses import asdict
from typing import Any, Dict

from app.services.token import TokenService
from app.tasks.hodler import create_token_hodlers_task
from app.ttypes.token import Token


class TokenController:
    def __init__(self) -> None:
        self.token_svc = TokenService()

    def create_token(self, payload: Dict[str, Any]) -> None:
        """Create Token in the database and then fetch all events since creation"""
        token = self.token_svc.create_token(payload)
        create_token_hodlers_task.apply_async(args=[asdict(token)])

    def get_token_by_name(self, name: str) -> Token:
        """Retrieve a Token row by its name"""
        return self.token_svc.get_token_by_name(name)

from typing import List

from app.models.hodler import HodlerModel
from app.services.hodler import HodlerService


class HodlerController:
    def __init__(self) -> None:
        self.svc = HodlerService()

    def find_top_hodler_by_token_name(self, token_name: str, limit: int = 100) -> List[HodlerModel]:
        """ Find all existing Hodlers by token """
        return self.svc.find_top_hodlers_by_token_name(token_name, limit=limit)

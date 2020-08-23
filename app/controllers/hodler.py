from typing import List

from app.models.hodler import Hodler
from app.services.hodler import HodlerService


class HodlerController:
    def __init__(self, hodler_svc: HodlerService) -> None:
        self.svc = hodler_svc

    def find_by_token_name(self, token_name: str) -> List[Hodler]:
        """ Find all existing Hodlers by token """
        return self.svc.find_by_token_name(token_name)

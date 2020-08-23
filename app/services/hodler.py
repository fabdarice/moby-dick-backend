from typing import Dict, List

from sqlalchemy.dialects.postgresql import insert

from app.models.hodler import HodlerModel
from app.ttypes.hodler import Hodler
from app.utils.session import SessionManager


class HodlerService:
    def __init__(self) -> None:
        pass

    def find_by_token_name(self, token_name: str) -> List[Hodler]:
        """ Find all existing Hodlers by token """
        with SessionManager.session() as session:
            rows = session.query(Hodler).filter(token_name=token_name).all()

        hodlers = [
            Hodler(
                address=row.address,
                number_transactions=row.number_transactions,
                amount=row.amount,
                token_name=row.token_name,
            )
            for row in rows
        ]

        return hodlers

    def save_hodlers(self, hodlers: List[Dict]) -> None:
        """ Save Hodlers in database """
        insert_stmt = insert(HodlerModel).values(hodlers)
        with SessionManager.use_connection() as c:
            c.execute(insert_stmt)

from typing import Any, Dict, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from app.models.hodler import HodlerModel
from app.ttypes.hodler import Hodler
from app.ttypes.token import Token
from app.utils.session import SessionManager


class HodlerService:
    def __init__(self) -> None:
        pass

    def find_top_hodlers_by_token_name(self, token_name: str, limit: int = 100) -> List[Hodler]:
        """ Find top Hodlers by token """
        with SessionManager.session() as session:
            rows = (
                session.query(HodlerModel)
                .filter_by(token_name=token_name)
                .order_by(HodlerModel.amount.desc())
                .limit(limit)
            )

            hodlers = [
                Hodler(
                    address=row.address,
                    number_transactions=row.number_transactions,
                    amount=row.amount,
                    token_name=row.token_name,
                    last_transaction=row.last_transaction,
                )
                for row in rows
            ]

            return hodlers

    def update_hodlers(self, hodlers_by_address: Dict[str, Any], token: Token) -> None:
        """ Update existing hodlers amount + Create if they do not exist yet """
        with SessionManager.session() as session:
            rows = (
                session.query(HodlerModel)
                .filter_by(token_name=token.name)
                .filter(HodlerModel.address.in_(list(hodlers_by_address.keys())))
                .all()
            )
            existing_hodlers = {row.address: row for row in rows}
            for hodler_addr, hodler in hodlers_by_address.items():
                if hodler_addr in existing_hodlers:
                    new_amount = int(hodler['amount']) + int(existing_hodlers[hodler_addr].amount)

                    hodler['amount'] = str(new_amount)
                    hodler['number_transactions'] += existing_hodlers[
                        hodler_addr
                    ].number_transactions

                hodler['amount'] = str(hodler['amount']).zfill(32)
                hodler['updated_at'] = func.current_timestamp()

        hodler_table = HodlerModel.__table__.c

        with SessionManager.use_connection() as c:
            stmt = insert(HodlerModel).values(list(hodlers_by_address.values()))
            stmt = stmt.on_conflict_do_update(
                constraint="hodler_address_token_unique",
                set_={
                    hodler_table.amount.name: stmt.excluded.amount,
                    hodler_table.number_transactions.name: stmt.excluded.number_transactions,
                    hodler_table.last_transaction.name: stmt.excluded.last_transaction,
                    hodler_table.updated_at.name: stmt.excluded.updated_at,
                },
            )
            c.execute(stmt)

from typing import Dict

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from app.models.watcher import WatcherModel
from app.utils.session import SessionManager


class WatcherService:
    def __init__(self) -> None:
        pass

    def upsert_watcher(self, payload: Dict[str, str]) -> None:
        table = WatcherModel.__table__.c

        payload['updated_at'] = func.current_timestamp()
        with SessionManager.use_connection() as c:
            stmt = insert(WatcherModel).values([payload])
            stmt = stmt.on_conflict_do_update(
                constraint="watchers_pkey",
                set_={
                    table.active.name: stmt.excluded.active,
                    table.alias.name: stmt.excluded.alias,
                    table.updated_at.name: stmt.excluded.updated_at,
                },
            )
            c.execute(stmt)

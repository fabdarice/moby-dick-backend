from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.borg import Borg


class SessionManagerBorg(Borg):
    def __init__(self) -> None:
        super().__init__()

        if not hasattr(self, 'db_url'):
            self.db_url: str = ''
            self.engine = None
            self._session = None

    @contextmanager
    def use_connection(self) -> Iterator:
        connection = self.engine.connect()  # type: ignore
        try:
            yield connection
        finally:
            connection.close()

    def configure(self, db_url: str) -> None:
        print('Configuring database..')
        self.db_url = db_url
        self.engine = create_engine(
            db_url, echo=False, use_batch_mode=True, connect_args={'connect_timeout': 1}
        )
        self.maker = sessionmaker(bind=self.engine)

    @contextmanager
    def session(self) -> Iterator:
        db_session = self.maker and self.maker()
        try:
            yield db_session
            db_session and db_session.flush()
            db_session and db_session.expunge_all()
            db_session and db_session.commit()
        except Exception:
            db_session and db_session.rollback()
            raise
        finally:
            db_session and db_session.close()


SessionManager = SessionManagerBorg()

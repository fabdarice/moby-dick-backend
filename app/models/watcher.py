from sqlalchemy import Column, String

from app.models.base import BaseModel


class WatcherModel(BaseModel):
    __table__ = 'watchers'

    address = Column(String(128), nullable=False, unique=True)

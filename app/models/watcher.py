from sqlalchemy import Boolean, Column, String

from app.models.base import BaseModel


class WatcherModel(BaseModel):
    __tablename__ = 'watchers'

    address = Column(String(128), primary_key=True)
    active = Column(Boolean)
    alias = Column(String(128))

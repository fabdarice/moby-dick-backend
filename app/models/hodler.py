from sqlalchemy import Column, Integer, String

from app.models.base import BaseModel


class Hodler(BaseModel):
    """
    This model represent a hodlers.
    """

    __tablename__ = 'hodlers'

    id = Column(Integer, primary_key=True)
    address = Column(String(128), index=True, unique=True, nullable=False)
    number_transactions = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=False)
    number_transactions = Column(Integer, nullable=False)
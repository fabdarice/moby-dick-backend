from sqlalchemy import Column, ForeignKey, Integer, String

from models.base import BaseModel
from models.hodler import Hodler


class TokenTranser(BaseModel):
    """
    This model represent a token transfer.
    """

    __tablename__ = 'token_transfers'

    id = Column(Integer, primary_key=True)
    seller_address = Column(String(128), ForeignKey(Hodler.address))
    buyer_address = Column(String(128), ForeignKey(Hodler.address))
    amount = Column(Integer, nullable=False)

    number_transactions = Column(Integer, nullable=True)

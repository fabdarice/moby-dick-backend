from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.schema import UniqueConstraint

from app.models.base import BaseModel
from app.models.token import TokenModel


class HodlerModel(BaseModel):
    """
    This model represent a hodlers.
    """

    __tablename__ = 'hodlers'

    id = Column(Integer, primary_key=True)
    address = Column(String(128), index=True, unique=False, nullable=False)
    number_transactions = Column(Integer, nullable=True)
    amount = Column(String(64), nullable=False)
    token_name = Column(String(8), ForeignKey(TokenModel.name))
    last_transaction = Column(String(128), nullable=True)

    __table_args__ = (
        UniqueConstraint('address', 'token_name', name='hodler_address_token_unique'),
    )

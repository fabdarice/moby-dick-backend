from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import BaseModel
from app.models.token import TokenModel


class HodlerModel(BaseModel):
    """
    This model represent a hodlers.
    """

    __tablename__ = 'hodlers'

    id = Column(Integer, primary_key=True)
    address = Column(String(128), index=True, unique=True, nullable=False)
    number_transactions = Column(Integer, nullable=True)
    amount = Column(String(64), nullable=False)
    token_name = Column(String(8), ForeignKey(TokenModel.name))

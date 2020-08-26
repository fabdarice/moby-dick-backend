from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import BaseModel


class TokenModel(BaseModel):
    """
    This model represent an attribute token.
    It contains a composite index for token and attribute name
    """

    __tablename__ = 'tokens'

    name = Column(String(128), primary_key=True)
    contract_address = Column(String(128), index=False, unique=True, nullable=False)
    uniswap_address = Column(String(128), index=False, unique=False, nullable=False)
    events = Column(String(800), nullable=False)
    synced = Column(Boolean, nullable=False)
    decimal = Column(Integer, nullable=False)
    total_supply = Column(Integer, nullable=True)

    last_block = Column(Integer, index=False, unique=False)
    block_creation = Column(Integer, index=False, unique=False)

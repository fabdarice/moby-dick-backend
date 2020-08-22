from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel


class Token(BaseModel):
    """
    This model represent an attribute token.
    It contains a composite index for token and attribute name
    """

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True, unique=False, nullable=False)
    contract_address = Column(String(128), index=False, unique=True, nullable=False)
    uniswap_address = Column(String(128), index=False, unique=False, nullable=False)
    events = Column(JSONB, nullable=False)

    last_block = Column(String(128), index=False, unique=False)
    block_creation = Column(String(128), index=False, unique=False)

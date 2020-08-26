from dataclasses import dataclass


@dataclass
class Hodler:
    address: str
    number_transactions: int
    amount: int
    token_name: str
    last_transaction: str

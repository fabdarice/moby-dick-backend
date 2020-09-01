from dataclasses import dataclass


@dataclass
class Watcher:
    address: str
    active: bool
    alias: str

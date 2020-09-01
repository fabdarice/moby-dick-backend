from typing import Dict

from app.services.watcher import WatcherService


class WatcherController:
    def __init__(self) -> None:
        self.watcher_svc = WatcherService()

    def upsert_watcher(self, payload: Dict[str, str]) -> None:
        self.watcher_svc.upsert_watcher(payload)

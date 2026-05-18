from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class IRefreshTokenRepository(ABC):
    @abstractmethod
    def create(self, user_fk: str, token: str, expires_at: datetime) -> None:
        ...

    @abstractmethod
    def find(self, token: str) -> Optional[dict]:
        ...

    @abstractmethod
    def update(self, token: str) -> None:
        ...

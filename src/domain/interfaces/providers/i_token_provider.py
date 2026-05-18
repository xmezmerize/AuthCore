from abc import ABC, abstractmethod
from datetime import datetime
from duckdi import Interface


@Interface(label="token")
class ITokenProvider(ABC):
    @abstractmethod
    def generate_access_token(self, id: str) -> str:
        ...
    
    @abstractmethod
    def generate_refresh_token(self, user_id: str) -> str:
        ...

    @abstractmethod
    def verify(self, token: str, is_refresh: bool = False) -> dict:
        ...

    @abstractmethod
    def get_expiration_from_token(self, token: str) -> datetime:
        ...

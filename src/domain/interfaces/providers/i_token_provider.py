from abc import ABC, abstractmethod
from duckdi import Interface


@Interface(label="token")
class ITokenProvider(ABC):
    @abstractmethod
    def generate(self, id: str) -> str:
        ...
    
    @abstractmethod
    def verify(self, token: str) -> dict:
        ...

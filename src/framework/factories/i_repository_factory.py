from domain.interfaces.repositories.i_user_repository import IUserRepository
from duckdi import Interface
from abc import ABC


@Interface(label="repository")
class IRepositoryFactory(ABC):
    def get_user_repository(self) -> IUserRepository:
        ...

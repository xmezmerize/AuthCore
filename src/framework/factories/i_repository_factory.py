from domain.interfaces.repositories.i_refresh_token_repository import IRefreshTokenRepository
from domain.interfaces.repositories.i_user_repository import IUserRepository
from duckdi import Interface
from abc import ABC


@Interface(label="repository")
class IRepositoryFactory(ABC):
    def get_user_repository(self) -> IUserRepository:
        ...

    def get_refresh_token_repository(self) -> IRefreshTokenRepository:
        ...

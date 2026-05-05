from domain.interfaces.repositories.i_user_repository import IUserRepository

from duckdi import Interface


@Interface(label="repository")
class IRepositoryFactory:
    def get_user_repository(self) -> IUserRepository:
        ...

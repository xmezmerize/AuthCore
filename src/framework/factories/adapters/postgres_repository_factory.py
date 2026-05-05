from adapters.repositories.postgres_user_repository import PostgresUserRepository
from domain.interfaces.repositories.i_user_repository import IUserRepository
from framework.factories.i_repository_factory import IRepositoryFactory


class PostgresRepositoryFactory(IRepositoryFactory):
    def get_user_repository(self) -> IUserRepository:
        return PostgresUserRepository()

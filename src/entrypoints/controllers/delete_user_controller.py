from domain.interfaces.providers.i_token_provider import ITokenProvider
from domain.usecases.users.delete_user_usecase import DeleteUserUsecase
from framework.factories.i_repository_factory import IRepositoryFactory

from duckdi import Get


class DeleteUserController:
    def delete(self, authorization: str) -> None:
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        token = Get(ITokenProvider, "token")

        return DeleteUserUsecase(factory, token).execute(authorization)

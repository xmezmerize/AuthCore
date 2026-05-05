from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.factories.i_repository_factory import IRepositoryFactory
from domain.usecases.users.find_user_usecase import FindUserUsecase

from dataclasses import asdict
from duckdi import Get


class FindUserController:
    def find(self, authorization: str):
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        token = Get(ITokenProvider, "token")
        found_user = FindUserUsecase(factory, token).execute(authorization)
        
        return found_user

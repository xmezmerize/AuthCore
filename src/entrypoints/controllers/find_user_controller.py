from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.factories.i_repository_factory import IRepositoryFactory
from domain.usecases.users.find_user_usecase import FindUserUsecase
from duckdi import Get


class FindUserController:
    def find(self, authorization: str, search: str = None):
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        token = Get(ITokenProvider, "token")
        
        usecase = FindUserUsecase(factory, token).execute(authorization, search)
        
        return usecase

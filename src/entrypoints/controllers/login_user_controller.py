from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.factories.i_repository_factory import IRepositoryFactory
from domain.usecases.users.login_user_usecase import LoginUserUsecase
from entrypoints.requests.login_user_request import LoginUserRequest
from domain.dtos.users.login_user_dto import LoginUserDto

from duckdi import Get


class LoginUserController:
    def login(self, request: LoginUserRequest) -> dict[str, str]:
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        password_hash = Get(IPasswordProvider, "password_hash")
        token = Get(ITokenProvider, "token")

        usecase = LoginUserUsecase(factory, password_hash, token)

        dto = LoginUserDto(
            email=request.email,
            password=request.password
        )

        return { "acess_token": usecase.execute(dto)}

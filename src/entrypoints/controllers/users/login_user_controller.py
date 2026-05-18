from domain.interfaces.providers.i_password_provider import IPasswordProvider
from entrypoints.requests.users.login_user_request import LoginUserRequest
from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.factories.i_repository_factory import IRepositoryFactory
from domain.usecases.users.login_user_usecase import LoginUserUsecase
from domain.dtos.users.login_user_dto import LoginUserDto
from fastapi import Response
from duckdi import Get


class LoginUserController:
    def login(self, request: LoginUserRequest, response: Response):
        factory = Get(IRepositoryFactory, "repository")
        user_repo = factory.get_user_repository()
        token_repo = factory.get_refresh_token_repository()
        
        password_hash = Get(IPasswordProvider, "password_hash")
        token_provider = Get(ITokenProvider, "token")

        usecase = LoginUserUsecase(user_repo, token_repo, password_hash, token_provider)
        
        dto = LoginUserDto(
            email=request.email,
            password=request.password
        )

        result = usecase.execute(dto)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth"
        )

        return {
            "access_token": result.access_token,
            "token_type": "Bearer"
        }

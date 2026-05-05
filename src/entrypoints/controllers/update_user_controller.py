from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.providers.i_token_provider import ITokenProvider
from domain.usecases.users.update_user_usecase import UpdateUserUsecase
from framework.factories.i_repository_factory import IRepositoryFactory
from entrypoints.requests.update_user_request import UpdateUserRequest
from domain.dtos.users.update_user_dto import UpdateUserDto
from domain.dtos.users.user_dto import UserDto

from typing import Optional
from duckdi import Get


class UpdateUserController:
    def update(self, user_id: str, request: UpdateUserRequest, authorization: str) -> Optional[UserDto]:
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        token = Get(ITokenProvider, "token")
        password = Get(IPasswordProvider, "password_hash")

        dto = UpdateUserDto(
            id=user_id,
            name=request.name,
            email=request.email
        )

        usecase = UpdateUserUsecase(factory, password, token)
        
        return usecase.execute(dto, authorization)

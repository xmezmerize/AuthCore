from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.usecases.users.create_user_usecase import CreateUserUsecase
from framework.factories.i_repository_factory import IRepositoryFactory
from entrypoints.requests.create_user_request import CreateUserRequest
from domain.dtos.users.create_user_dto import CreateUserDto
from duckdi import Get


class CreateUserController:
    def create(self, request: CreateUserRequest):
        factory = Get(IRepositoryFactory, "repository").get_user_repository()
        password_provider = Get(IPasswordProvider, "password_hash")
        
        usecase = CreateUserUsecase(factory, password_provider)

        dto = CreateUserDto(
            name=request.name,
            email=request.email,
            password=request.password
        )

        return usecase.execute(dto)

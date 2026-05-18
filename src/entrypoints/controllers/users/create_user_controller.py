from domain.interfaces.providers.i_password_provider import IPasswordProvider
from entrypoints.requests.users.create_user_request import CreateUserRequest
from domain.usecases.users.create_user_usecase import CreateUserUsecase
from framework.factories.i_repository_factory import IRepositoryFactory
from domain.dtos.users.create_user_dto import CreateUserDto
from duckdi import Get


class CreateUserController:
    def create(self, request: CreateUserRequest):
        factory = Get(IRepositoryFactory, "repository")
        password_provider = Get(IPasswordProvider, "password_hash")
        
        user_repo = factory.get_user_repository()

        usecase = CreateUserUsecase(
            user_repository=user_repo, 
            password_provider=password_provider, 
        )

        dto = CreateUserDto(
            name=request.name,
            email=request.email,
            password=request.password
        )

        return usecase.execute(dto)

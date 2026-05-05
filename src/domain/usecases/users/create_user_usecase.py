from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from entrypoints.responses.user_response import UserResponse
from domain.dtos.users.create_user_dto import CreateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from domain.dtos.users.user_dto import UserDto


class CreateUserUsecase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_provider: IPasswordProvider
    ):
        self.user_repository = user_repository
        self.password_provider = password_provider
    
    def execute(self, dto: CreateUserDto) -> UserDto:
        user_already_exists = self.user_repository.find(
            FindUserDto(email=dto.email)
            )
        
        if len(user_already_exists) > 0:
            raise NameError("Error: This user couldn't be created! This email already in use...")
        
        if len(dto.password) == 0:
            raise NameError("Error: This user couldn't be created! The password cannot be empty...")
        
        dto.password = self.password_provider.hash(dto.password)

        user = self.user_repository.create(dto)

        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            message="This user was created!"
        )

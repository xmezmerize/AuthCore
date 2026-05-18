from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from entrypoints.responses.users.user_response import UserResponse
from domain.dtos.users.create_user_dto import CreateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from domain.dtos.users.user_dto import UserDto


class CreateUserUsecase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_provider: IPasswordProvider,
    ):
        self.user_repository = user_repository
        self.password_provider = password_provider
    
    def execute(self, dto: CreateUserDto) -> UserDto:
        verify_user = self.user_repository.find(FindUserDto(email=dto.email))
        
        if len(verify_user) > 0:
            raise NameError(f"Erro: Já existe um usuário com o email {dto.email}")
        
        if len(dto.password) == 0:
            raise NameError("Erro: A senha não pode ser vazia")
        
        dto.password = self.password_provider.hash(dto.password)
        
        row = self.user_repository.create(dto)

        return UserResponse(
            id=str(row.id),
            name=row.name,
            email=row.email,
            created_at=row.created_at,
            updated_at=row.updated_at,
            message="Usuário criado com sucesso!"
        )

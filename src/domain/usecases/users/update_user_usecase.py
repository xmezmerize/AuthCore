from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.user_response import UserResponse
from domain.dtos.users.update_user_dto import UpdateUserDto


class UpdateUserUsecase:
    def __init__(
            self,
        user_repository: IUserRepository,
        password_provider: IPasswordProvider,
        token_provider: ITokenProvider
    ):
        self.user_repository = user_repository
        self.password_provider = password_provider
        self.token_provider = token_provider
        
    def execute(self, dto: UpdateUserDto, token: str):
        token_decoded = self.token_provider.verify(token)
        id = token_decoded.get("sub")

        if id != dto.id:
            raise NameError("Erro: UpdateUserUsecase (-> sub <-)")

        row = self.user_repository.update(dto.id, dto)

        return UserResponse(
             id=str(row.id),
             name=row.name, 
             email=row.email,
             created_at=row.created_at,
             updated_at=row.updated_at,
             message="Usuário atualizado com sucesso!"
             )

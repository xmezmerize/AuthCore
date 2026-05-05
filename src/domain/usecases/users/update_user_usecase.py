from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from entrypoints.responses.user_response import UserResponse
from domain.dtos.users.update_user_dto import UpdateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from domain.dtos.users.user_dto import UserDto
from typing import Optional


class UpdateUserUsecase:
    def __init__(
            self,
            user_repository: IUserRepository,
            password_provider: IPasswordProvider
            ):
            self.user_repository = user_repository
            self.password_provider = password_provider
        
    def execute(self, dto: UpdateUserDto, token_str: str):
        # 1. Valida o token
        decoded = self.token.verify(token_str)
        user_id_from_token = decoded.get("sub")

        # 2. Segurança: Um usuário só pode editar a si mesmo?
        if user_id_from_token != dto.id:
            raise ValueError("Você não tem permissão para alterar outro usuário")

        # 3. Chama o repositório
        updated_user = self.repository.update(dto)
        return UserResponse(id=str(updated_user.id), name=updated_user.name, message="Atualizado com sucesso")

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
        decoded = self.token_provider.verify(token)
        user_id_from_token = decoded.get("sub")

        if user_id_from_token != dto.id:
            raise ValueError("You cannot update this user!")

        updated_user = self.user_repository.update(dto.id, dto)
        return UserResponse(
             id=str(updated_user.id),
             name=updated_user.name, 
             email=updated_user.email,
             message="Updated with success!"
             )

from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.user_response import UserResponse


class DeleteUserUsecase:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_provider: ITokenProvider
    ):
        self.user_repository = user_repository
        self.token_provider = token_provider

    def execute(self, id: str, token: str) -> UserResponse:
        decoded = self.token_provider.verify(token)
        user_id_from_token = decoded.get("sub")

        if str(user_id_from_token) != str(id):
            return UserResponse(
                id=id,
                name="",
                email="",
                message="You can only delete your own account!"
            )

        deleted = self.user_repository.delete(id)

        if deleted:
            return UserResponse(
                id=id, 
                message="This user was deleted!"
            )
        
        return UserResponse(
            id=id,
            message="User not found or cannot be deleted."
        )

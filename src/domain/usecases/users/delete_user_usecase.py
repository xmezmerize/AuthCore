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

    def execute(self, id: str, token: str) -> None:
        if self.token_provider.verify(token):
            deleted = self.user_repository.delete(id)

            if deleted:
                return UserResponse(
                    id=id, 
                    name="", 
                    email="", 
                    message="This user was deleted!"
                )
            
            return UserResponse(
                id=id, 
                name="", 
                email="", 
                message="User not found or cannot be deleted."
            )
        raise ValueError("Invalid Credentials!")

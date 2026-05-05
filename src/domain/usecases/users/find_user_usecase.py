from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.user_response import UserResponse
from domain.dtos.users.find_user_dto import FindUserDto


class FindUserUsecase:
    def __init__(
            self,
            repository: IUserRepository,
            token: ITokenProvider
            ):
            self.user_repository = repository
            self.token_provider = token
    
    def execute(self, authorization: str) -> list[UserResponse]:
        decoded_token = self.token_provider.verify(authorization)
        if decoded_token:
            user_id = decoded_token.get("sub")
            dto = FindUserDto(id=user_id)

            found = self.user_repository.find(dto)

            return [
                UserResponse(
                    id=str(find.id), 
                    name=find.name, 
                    email=find.email,
                    created_at=find.created_at,
                    updated_at=find.updated_at
                ) for find in found
            ]
        
        raise ValueError("Error: Invalid token...")

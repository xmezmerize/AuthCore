from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.users.user_response import UserResponse
from framework.helpers.verify_helpers import verify_helpers
from domain.dtos.users.find_user_dto import FindUserDto


class FindUserUsecase:
    def __init__(
        self,
        repository: IUserRepository,
        token: ITokenProvider
    ):
        self.user_repository = repository
        self.token_provider = token
        self.helpers = verify_helpers
    
    def execute(self, authorization: str, search: str = None) -> list[UserResponse]:
        token_decoded = self.token_provider.verify(authorization)
        if not token_decoded:
            raise NameError("Erro: Token inválido ou expirado...")

        if search:
            is_uuid = self.helpers._is_valid_uuid(search)
            date = self.helpers._try_parse_date(search)

            dto = FindUserDto(
                id=search if is_uuid else None,
                name=search,
                email=search,
                created_at=date, 
                updated_at=date
            )
        else:
            dto = FindUserDto()

        rows = self.user_repository.find(dto)
        return [
            UserResponse(
                id=str(row.id), 
                name=row.name, 
                email=row.email,
                created_at=row.created_at,
                updated_at=row.updated_at
            ) for row in rows
        ]

from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.user_response import UserResponse
from domain.dtos.users.find_user_dto import FindUserDto
from datetime import datetime
import uuid


class FindUserUsecase:
    def __init__(
            self,
            repository: IUserRepository,
            token: ITokenProvider
        ):
            self.user_repository = repository
            self.token_provider = token
    
    def execute(self, authorization: str, search: str = None) -> list[UserResponse]:
        token_decoded = self.token_provider.verify(authorization)
        if not token_decoded:
            raise NameError("Erro: FindUserUsecase (-> token_decoded <-) token inválido ou expirado...")

        if search:
            is_uuid = self._is_valid_uuid(search)
            date = self._try_parse_date(search)

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

    def _is_valid_uuid(self, value: str) -> bool:
        try:
            uuid.UUID(str(value))
            return True
        except:
            return False

    def _try_parse_date(self, value: str):
        if not value: return None
        clean_value = value.replace('\\', '').strip().split(' ')[0] 
        
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d'):
            try:
                return datetime.strptime(clean_value, fmt).date()
            except ValueError:
                continue
        return None

from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from entrypoints.responses.users.user_response import UserResponse


class DeleteUserUsecase:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_provider: ITokenProvider
    ):
        self.user_repository = user_repository
        self.token_provider = token_provider

    def execute(self, id: str, token: str) -> UserResponse:
        token_decoded = self.token_provider.verify(token)
            
        if not token_decoded:
            raise NameError("Erro: Token inválido ou expirado...")
        
        id = token_decoded.get("sub")

        row = self.user_repository.delete(id)

        if row:
            return UserResponse(
                id=id, 
                message="O usuário foi deletado com sucesso!"
            )
        return UserResponse(
            id=id,
            message="O usuário não foi encontrado ou não pôde ser excluído!"
        )

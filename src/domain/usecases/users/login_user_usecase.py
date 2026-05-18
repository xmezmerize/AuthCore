from domain.interfaces.repositories.i_refresh_token_repository import IRefreshTokenRepository
from entrypoints.responses.refresh_token.refresh_token_response import RefreshTokenResponse
from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from domain.dtos.users.login_user_dto import LoginUserDto
from domain.dtos.users.find_user_dto import FindUserDto


class LoginUserUsecase:
    def __init__(
        self,
        repository: IUserRepository,
        token_repository: IRefreshTokenRepository,
        password_provider: IPasswordProvider,
        token_provider: ITokenProvider
    ):
        self.repository = repository
        self.token_repository = token_repository
        self.password_provider = password_provider
        self.token_provider = token_provider

    def execute(self, dto: LoginUserDto) -> RefreshTokenResponse:
        verify_user = self.repository.find(FindUserDto(email=dto.email))
    
        if not verify_user:
            raise NameError("Erro: Email não encontrado")
    
        user = verify_user[0]

        if not self.password_provider.verify(dto.password, user.password):
            raise NameError("Erro: Senha inválida")

        access_token = self.token_provider.generate_access_token(user.id)
        refresh_token = self.token_provider.generate_refresh_token(user.id)

        self.token_repository.create(
            user_fk=str(user.id),
            token=refresh_token,
            expires_at=self.token_provider.get_expiration_from_token(refresh_token)
        )

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

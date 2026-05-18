from domain.interfaces.repositories.i_refresh_token_repository import IRefreshTokenRepository
from entrypoints.responses.refresh_token.refresh_token_response import RefreshTokenResponse
from entrypoints.requests.refresh_token.refresh_token_request import RefreshTokenRequest
from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.helpers.exceptions import UnauthorizedError
from datetime import datetime, timezone


class RefreshTokenUsecase:
    def __init__(
        self,
        refresh_token_repository: IRefreshTokenRepository,
        token_provider: ITokenProvider
    ):
        self.refresh_token_repository = refresh_token_repository
        self.token_provider = token_provider

    def execute(self, request: RefreshTokenRequest) -> RefreshTokenResponse:
        payload = self.token_provider.verify(request.refresh_token, is_refresh=True)
        user_fk = payload.get("sub")

        db_token = self.refresh_token_repository.find(request.refresh_token)
        now = datetime.now(timezone.utc)

        if not db_token or db_token.is_revoked:
            raise UnauthorizedError("Token inválido ou já utilizado.")

        expires_at = db_token.expires_at.replace(tzinfo=timezone.utc) if db_token.expires_at.tzinfo is None else db_token.expires_at
        
        if expires_at < now:
            raise UnauthorizedError("Sessão expirada.")

        self.refresh_token_repository.update(request.refresh_token)

        new_access = self.token_provider.generate_access_token(user_fk)
        new_refresh = self.token_provider.generate_refresh_token(user_fk)
        new_expires_at = self.token_provider.get_expiration_from_token(new_refresh)

        self.refresh_token_repository.create(user_fk, new_refresh, new_expires_at)

        return RefreshTokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="Bearer"
        )

from entrypoints.requests.refresh_token.refresh_token_request import RefreshTokenRequest
from domain.usecases.refresh_token.refresh_token_usecase import RefreshTokenUsecase
from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.factories.i_repository_factory import IRepositoryFactory
from framework.helpers.exceptions import UnauthorizedError
from fastapi import Request, Response
from duckdi import Get


class RefreshTokenController:
    def refresh(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")
        
        if not refresh_token:
            raise UnauthorizedError("Erro: O refresh token não encontrado nos cookies.")

        factory = Get(IRepositoryFactory, "repository")
        token_repo = factory.get_refresh_token_repository()
        token_provider = Get(ITokenProvider, "token")

        dto = RefreshTokenRequest(refresh_token=refresh_token) 
        
        usecase = RefreshTokenUsecase(token_repo, token_provider)
        result = usecase.execute(dto)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth"
        )

        return {
            "access_token": result.access_token,
            "token_type": "Bearer"
        }

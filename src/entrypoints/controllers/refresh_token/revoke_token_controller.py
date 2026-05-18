from framework.factories.i_repository_factory import IRepositoryFactory
from fastapi import Request, Response
from duckdi import Get


class RevokeTokenController:
    def revoke(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            return {"message": "Nenhum token ativo encontrado"}

        factory = Get(IRepositoryFactory, "repository")
        token_repository = factory.get_refresh_token_repository()
        token_repository.update(refresh_token)
        
        response.delete_cookie(
            key="refresh_token",
            path="/auth"
        )
        
        return {"message": "Token revogado com sucesso"}

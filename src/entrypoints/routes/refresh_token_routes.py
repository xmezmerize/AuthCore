from entrypoints.controllers.refresh_token.refresh_token_controller import RefreshTokenController
from entrypoints.controllers.refresh_token.revoke_token_controller import RevokeTokenController
from fastapi import APIRouter, Request, Response

route = APIRouter(prefix="/auth")


@route.post("/refresh")
async def refresh(request: Request, response: Response):
    return RefreshTokenController().refresh(request, response)

@route.post("/revoke")
async def revoke(request: Request, response: Response):
    return RevokeTokenController().revoke(request, response)

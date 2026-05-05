from fastapi import HTTPException, Request


class HandlerJwt:
    def get_jwt_from_request(self, request: Request) -> str:
        authorization = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(status_code=401, detail="Header ausente")
        
        if authorization.startswith("Bearer "):
            return authorization.replace("Bearer ", "")
        
        return authorization

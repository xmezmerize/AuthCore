from domain.interfaces.providers.i_token_provider import ITokenProvider
from datetime import datetime, timedelta, timezone
import jwt
import os


class JwtTokenProvider(ITokenProvider):
    def __init__(self) -> None:
        self.expires_hours = int(os.getenv("JWT_EXPIRES_IN", 1))

        secret = os.getenv("JWT_SECRET", None)
        if secret is None or len(secret) == 0:
            raise EnvironmentError("Não foi encontrado: \"JWT_SECRET\" ENV!")
        
        self.secret = secret
        
    def generate(self, id: str) -> str:
       now = datetime.now(timezone.utc)

       payload = {
           "sub": id,
           "iat": now,
           "exp": now + timedelta(hours=self.expires_hours)
       }
       return jwt.encode(payload, self.secret, algorithm="HS256")
    
    def verify(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=["HS256"])

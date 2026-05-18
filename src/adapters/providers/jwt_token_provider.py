from domain.interfaces.providers.i_token_provider import ITokenProvider
from framework.helpers.exceptions import UnauthorizedError
from datetime import datetime, timedelta, timezone
import jwt
import os


class JwtTokenProvider(ITokenProvider):
    def __init__(self) -> None:
        self.access_expires = int(os.getenv("JWT_EXPIRES_IN", 1))
        self.refresh_expires = int(os.getenv("JWT_REFRESH_EXPIRES_IN", 168))

        self.secret = os.getenv("JWT_SECRET")
        self.refresh_secret = os.getenv("JWT_REFRESH_SECRET")

        if not self.secret:
            raise EnvironmentError("Não foi encontrado: \"JWT_SECRET\" ENV!")
        if not self.refresh_secret:
            raise EnvironmentError("Não foi encontrado: \"JWT_REFRESH_SECRET\" ENV!")

    def generate_access_token(self, id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": id,
            "iat": now,
            "exp": now + timedelta(hours=self.access_expires),
            "type": "access"
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def generate_refresh_token(self, id: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": id,
            "iat": now,
            "exp": now + timedelta(hours=self.refresh_expires),
            "type": "refresh"
        }
        return jwt.encode(payload, self.refresh_secret, algorithm="HS256")

    def verify(self, token: str, is_refresh: bool = False) -> dict:
        secret = self.refresh_secret if is_refresh else self.secret
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token expirado.")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Token inválido.")

    def get_expiration_from_token(self, token: str) -> datetime:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = payload.get("exp")
            
            if not exp_timestamp:
                raise ValueError("Token não possui campo de expiração (exp)")

            return datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        except Exception as e:
            raise ValueError(f"Erro ao extrair expiração do token: {str(e)}")

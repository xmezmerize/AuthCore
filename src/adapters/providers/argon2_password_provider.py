from domain.interfaces.providers.i_password_provider import IPasswordProvider
from argon2 import PasswordHasher


class Argon2PasswordProvider(IPasswordProvider):
    def hash(self, password: str) -> str:
        return PasswordHasher().hash(password)
    
    def verify(self, password: str, hash: str) -> bool:
        try:
            return PasswordHasher().verify(hash, password)
        except:
            raise ValueError("Error: Invalid Credentials!")

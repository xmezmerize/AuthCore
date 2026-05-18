from domain.interfaces.providers.i_password_provider import IPasswordProvider
from argon2 import PasswordHasher


class Argon2PasswordProvider(IPasswordProvider):
    def __init__(self):
        self.hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self.hasher.hash(password)
    
    def verify(self, password: str, hash: str) -> bool:
        try:
            return self.hasher.verify(hash, password)
        except:
            raise NameError("Erro interno: Não foi possível fazer login, pois a senha usada é inválida!")

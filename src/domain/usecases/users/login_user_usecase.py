from domain.interfaces.providers.i_password_provider import IPasswordProvider
from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.interfaces.providers.i_token_provider import ITokenProvider
from domain.dtos.users.login_user_dto import LoginUserDto
from domain.dtos.users.find_user_dto import FindUserDto


class LoginUserUsecase:
    def __init__(
        self,
        repository: IUserRepository,
        password_provider: IPasswordProvider,
        token_provider: ITokenProvider
    ):
        self.repository = repository
        self.password_provider = password_provider
        self.token_provider = token_provider
    
    def execute(self, dto: LoginUserDto) -> str:
        verify_user = self.repository.find(FindUserDto(email=dto.email))
        if not verify_user:
            raise NameError("Erro: LoginUserUsecase (-> dto.email <-) email não encontrado ou inválido")
        
        user = verify_user[0]

        is_password_valid = self.password_provider.verify(dto.password, user.password)

        if not is_password_valid:
            raise NameError("Erro: LoginUserUsecase (-> is_password_valid <-) senha inválida")

        return self.token_provider.generate(user.id)

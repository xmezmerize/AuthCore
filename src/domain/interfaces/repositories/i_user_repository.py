from abc import ABC, abstractmethod
from typing import Optional

from domain.dtos.users.create_user_dto import CreateUserDto
from domain.dtos.users.update_user_dto import UpdateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from domain.dtos.users.user_dto import UserDto


class IUserRepository(ABC):
    @abstractmethod
    def create(self, dto: CreateUserDto) -> UserDto:
        ...
    
    @abstractmethod
    def find(self, dto: FindUserDto = FindUserDto()) -> list[UserDto]:
        ...
    
    @abstractmethod
    def update(self, id: str, dto: UpdateUserDto) -> Optional[UserDto]:
        ...
    
    @abstractmethod
    def delete(self, id: str) -> None:
        ...

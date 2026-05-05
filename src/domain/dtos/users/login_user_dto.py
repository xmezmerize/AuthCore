from dataclasses import dataclass


@dataclass
class LoginUserDto:
    email: str
    password: str

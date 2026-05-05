from dataclasses import dataclass
from typing import Optional


@dataclass
class UpdateUserDto:
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

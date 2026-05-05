from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserDto:
    id: str
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime

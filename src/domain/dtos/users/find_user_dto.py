from dataclasses import dataclass
from typing import Optional


@dataclass
class FindUserDto:
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

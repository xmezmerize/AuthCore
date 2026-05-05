from typing import Optional

from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    message: Optional[str] = None

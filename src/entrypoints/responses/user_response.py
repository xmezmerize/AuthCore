from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional
import os

class UserResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    message: Optional[str] = None

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, dt: datetime):
        if dt is None:
            return None
        fmt = os.getenv("BRAZILIAN_DATE_FORMAT", "%d/%m/%Y %H:%M:%S")
        return dt.strftime(fmt)
    
    model_config = {
        "from_attributes": True
    }

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshTokenDto:
    id: str
    token: str
    user_fk: str
    expires_at: datetime
    is_revoked: bool

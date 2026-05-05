from pydantic import BaseModel


class FindUserRequest(BaseModel):
    token: str

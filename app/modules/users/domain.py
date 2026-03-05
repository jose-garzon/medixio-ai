from typing import Optional

from pydantic import BaseModel


class UserMessenger(BaseModel):
    messenger_id: int
    first_name: str
    last_name: Optional[str]


class User(UserMessenger):
    id: int

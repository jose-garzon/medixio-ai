from datetime import datetime

from sqlmodel import Field, SQLModel

from app.lib.dates import get_current_timestamp


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    messenger_id: str = Field(unique=True)
    name: str
    phone_number: str
    created_at: datetime = Field(default_factory=get_current_timestamp)

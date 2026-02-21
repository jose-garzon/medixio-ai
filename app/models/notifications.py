from datetime import datetime

from app.lib.dates import get_current_timestamp
from sqlmodel import Field, SQLModel


class Notification(SQLModel):
    id: int = Field(default=None, primary_key=True)
    scheduled_time: datetime
    sent: bool
    message: str
    created_at: datetime = Field(default_factory=get_current_timestamp)

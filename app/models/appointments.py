from datetime import datetime
from enum import Enum

from app.lib.dates import get_current_timestamp
from sqlmodel import Field, SQLModel


class AppointmentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DONE = "done"
    MISSED = "missed"
    LOST = "lost"


class Appointment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    doctor_name: str
    doctor_phone_number: str
    specialty: str
    address: str
    due_date: datetime
    status: AppointmentStatus
    created_at: datetime = Field(default_factory=get_current_timestamp)
    updated_at: datetime = Field(
        default_factory=get_current_timestamp,
        sa_column_kwargs={"onupdate": get_current_timestamp},
    )

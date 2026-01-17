
from fastapi import APIRouter
from services import appointment_reminder_service

router = APIRouter()

@router.get("/appointment_reminders")
def get_appointment_reminders():
    return appointment_reminder_service.get_all_appointment_reminders()

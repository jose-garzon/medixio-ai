
from fastapi import APIRouter
from services import medication_reminder_service

router = APIRouter()

@router.get("/medication_reminders")
def get_medication_reminders():
    return medication_reminder_service.get_all_medication_reminders()

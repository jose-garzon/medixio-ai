
from fastapi import APIRouter
from services import appointment_service

router = APIRouter()

@router.get("/appointments")
def get_appointments():
    return appointment_service.get_all_appointments()

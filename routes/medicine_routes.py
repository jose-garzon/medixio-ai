
from fastapi import APIRouter
from services import medicine_service

router = APIRouter()

@router.get("/medicines")
def get_medicines():
    return medicine_service.get_all_medicines()

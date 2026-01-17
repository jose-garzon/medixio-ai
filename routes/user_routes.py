
from fastapi import APIRouter
from services import user_service

router = APIRouter()

@router.get("/users")
def get_users():
    return user_service.get_all_users()

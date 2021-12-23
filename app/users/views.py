from fastapi import APIRouter
from .models import User
from .scheams import UserResponse
from typing import List, Optional



router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/list/', response_model=List[UserResponse])
def get_user_list():
    qs = User.objects.all()
    return list(qs)
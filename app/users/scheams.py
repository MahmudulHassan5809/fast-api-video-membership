from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr
from pydantic.types import conint



class UserResponse(BaseModel):
    # user_id: str
    email: str

    class Config:
        orm_mode = True
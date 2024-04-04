# models.py
# Pydantic models go here (not DB models) 

from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
import re
import bcrypt
from ..auth.models import RoleEnum, User
from datetime import datetime

from ..utils.utils import validate_url


class PetLineCreate(BaseModel):
    production_line_id: Annotated[str, Field(..., examples=["12132fasdas23r1f"])]
    name: Annotated[str, Field(max_length=100)]
    photo_url: Optional[str] = None
    flavors: Annotated[list[str], Field(..., examples=[["chicken", "beef"]])]
    sizes: Annotated[list[str], Field(..., examples=[["small", "medium"]])]


    @validator("photo_url")
    def validate_photo_url(cls, v):
        return validate_url(v)

class PetLineUpdate(PetLineCreate):
    pass

class PetLineInDB(PetLineCreate):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: datetime
    updated_at: datetime

class PetLine(PetLineCreate):
    id: Optional[str]
    created_at: datetime
    updated_at: datetime
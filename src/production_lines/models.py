# models.py
# Pydantic models go here (not DB models) 

from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
import re
import bcrypt
from ..auth.models import RoleEnum, User
from datetime import datetime


class ProductionLineCreate(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    photo_url: Optional[str] = None

    @validator("photo_url")
    def validate_photo_url(cls, v):
        return validate_url(v)

class ProductionLineUpdate(ProductionLineCreate):
    pass

class ProductionLineInDB(ProductionLineCreate):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: datetime
    updated_at: datetime

class ProductionLine(ProductionLineCreate):
    id: Optional[str]
    created_at: datetime
    updated_at: datetime
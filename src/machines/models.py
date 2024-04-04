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


class MachineCreate(BaseModel):
    pet_line_id: Annotated[str, Field(..., examples=["12132fasdas23r1f"])]
    name: Annotated[str, Field(max_length=100)]


class MachineUpdate(MachineCreate):
    pass

class MachineInDB(MachineCreate):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: datetime
    updated_at: datetime

class Machine(MachineCreate):
    id: Optional[str]
    created_at: datetime
    updated_at: datetime
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


class CounterCreate(BaseModel):
    machine_id: Annotated[str, Field(..., examples=["12132fasdas23r1f"])]
    name: Annotated[str, Field(max_length=100)]


class CounterUpdate(CounterCreate):
    pass

class CounterInDB(CounterCreate):
    id: Optional[str] = Field(alias='_id', default=None)
    created_at: datetime
    updated_at: datetime

class Counter(CounterCreate):
    id: Optional[str]
    created_at: datetime
    updated_at: datetime
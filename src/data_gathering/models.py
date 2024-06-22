# models.py
# Pydantic models go here (not DB models) 

from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
import re
import bcrypt
from ..auth.models import RoleEnum, User
from datetime import datetime
from fastapi import FastAPI, File, UploadFile

from ..utils.utils import validate_url


class OcrModelCreate(BaseModel):
    counter_id: str
    file_name: str
    collected_info: list[str] = []
    created_at: datetime
    updated_at: datetime


class OcrModelInDB(OcrModelCreate):
    id: Optional[str] = Field(alias='_id', default=None)
    file_path: str | None = None

class OcrModelUpdate(OcrModelCreate):
    file_path: str | None = None

class OcrModel(OcrModelCreate):
    id: Optional[str]
    file_path: str | None = None

class OcrModelResponse(OcrModel):
    pass


class Data(BaseModel):
    counter_id: str
    ocr_model_id: str | None
    flavor: str
    size: str
    collected_info_values: object
    uploader_username: str
    created_at: datetime
    updated_at: datetime

class DataResponse(Data):
    id: str
    file_url: Optional[str] = None

class DataInDB(Data):
    id: Optional[str] = Field(alias='_id', default=None)
    file_url: Optional[str] = None

class DataUpdate(Data):
    pass


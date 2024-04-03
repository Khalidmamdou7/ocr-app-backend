# Global Pydantic models (e.g. ResponseModel, etc.)

from typing import Generic, TypeVar, Annotated
from enum import Enum

from pydantic import BaseModel, Field

# Generic type for any object
T = TypeVar("T")

# Define enum for response status
class ResponseStatus(str, Enum):
    success = 'success'
    error = 'error'

class ResponseModel(BaseModel, Generic[T]):
    status: Annotated[ResponseStatus, Field(..., example='success')]
    message: Annotated[str, Field(..., example='User created successfully')]
    data: T | None = None
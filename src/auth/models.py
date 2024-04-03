# models.py
# Pydantic models go here (not DB models) 

from enum import Enum as PyEnum
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Annotated
import re

class RoleEnum(str, PyEnum):
    ADMIN = 'Admin' # Note: If you change this, you might broke creating the admin as it checks for this value before creating one (see auth/service.py/create_admin_user)
    MANAGER = 'Manager'
    WORKER = 'Worker'


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    team: Optional[str] = None


class User(BaseModel):
    username: Annotated[str, Field(..., min_length=3, examples=['johndoe'])] = "dummy_username"
    email: EmailStr | None = "dummy_email@mail.com"
    full_name: Annotated[str, Field(..., min_length=3, max_length=50, examples=['John Doe'])] = "dummy_full_name"
    mobile: Annotated[str, Field(..., min_length=11, max_length=11, pattern=r'^01\d{9}$', examples=['01234567890'])] = "01234567890"
    role: Annotated[RoleEnum, Field(..., examples=['team_member'])] = RoleEnum.TEAM_MEMBER

class UserInDB(User):
    id: Optional[str] = Field(alias='_id', default=None)
    disabled: bool = True
    hashed_password: str
    team: Optional[str] = None

class UserResponse(User):
    id: Optional[str]
    team: Optional[str] = None


class UserCreateRequest(BaseModel):
    username: Annotated[str, Field(..., min_length=3, examples=['johndoe'])] = "johndoe"
    email: EmailStr | None = "johndoe@gmail.com"
    full_name: Annotated[str, Field(..., min_length=3, max_length=50, examples=['John Doe'])] = "John Doe"
    mobile: Annotated[str, Field(..., min_length=11, max_length=11, pattern=r'^01\d{9}$', examples=['01234567890'])] = "01234567890"
    password: Annotated[str, Field(..., min_length=8, examples=['password123'])]


class UserCreateResponse(User):
    pass

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: Annotated[str, Field(..., min_length=8, examples=['password123'])]

# Pydantic model for user login request
class UserLogin(BaseModel):
    # This can be username, email, or mobile number
    identifier: Annotated[str, Field(..., examples=['johndoe'])]
    password: Annotated[str, Field(..., min_length=8, examples=['password123'])]


    @validator('identifier')
    def identifier_validator(cls, value):
        # Check if the identifier is a valid number
        if value.isdigit():
            # Allowing only the Egyptian mobile numbers
            pattern = r'^01\d{9}$'
            if len(value) != 11 or not re.match(pattern, value):
                raise ValueError('Mobile number is not valid, must be 11 digits and start with 01')
            return value
        # Otherwise, it is a username or email
        else:
            if len(value) < 3:
                raise ValueError('Username must be at least 3 characters')
            return value
                

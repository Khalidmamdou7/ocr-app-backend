# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel

# An example of importing sth from the same directory (importing the whole file as module)
from . import service as auth_service

# An example of importing sth from the same directory (importing specific functinos from the file)
from .dependencies import authenticate_user_jwt, get_current_user

from .models import *


router = APIRouter()


@router.post("/register", response_model=ResponseModel[UserCreateResponse], status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateRequest):
    user = await auth_service.create_user(user)
    return {
        "status": "success",
        "message": "Account created successfully, Please confirm your email to login",
        "data": user
    }


@router.post("/login", response_model=ResponseModel[Token])
def login_for_access_token(user: UserLogin):
    data = auth_service.login(user.identifier, user.password)
    return {"status": "success", "message": "Login successful", "data": data}

# TODO: Will be redirected to the frontend
@router.get("/confirm/{token}", response_model=ResponseModel[None])
async def confirm_email(email: EmailStr, token: str):
    auth_service.confirm_email(email, token)
    return {"status": "success", "message": "Email confirmed successfully", "data": None}

@router.post("/resend-confirmation-email", response_model=ResponseModel[None])
async def resend_confirmation_email(email: EmailStr):
    await auth_service.resend_confirmation_email(email)
    return {"status": "success", "message": "Confirmation email resent successfully", "data": None}

@router.post("/forgot-password", response_model=ResponseModel[None])
def forgot_password(email: EmailStr):
    auth_service.forgot_password(email)
    return {"status": "success", "message": "Password reset link sent successfully", "data": None}

# request body will contain token and new password and email
@router.post("/reset-password", response_model=ResponseModel[None])
def reset_password(request: ResetPasswordRequest):
    auth_service.reset_password(request.email, request.token, request.new_password)
    return {"status": "success", "message": "Password reset successfully", "data": None}

@router.get("/users/me/", response_model=ResponseModel[UserResponse], tags=["users"])
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
):
    return {"status": "success", "message": "User details retrieved successfully", "data": current_user}


@router.get("/assign-role/{user_identifier}", response_model=ResponseModel[UserResponse], tags=["admin"])
async def assign_role(
    user_identifier: str,
    role: RoleEnum,
    current_user: Annotated[UserResponse, Depends(authenticate_user_jwt)]
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the permission to perform this action",
        )
    return {"status": "success", "message": "Role assigned successfully", "data": auth_service.assign_role(user_identifier, RoleEnum(role))}


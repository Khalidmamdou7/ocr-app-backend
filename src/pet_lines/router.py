# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as production_line_service
from .models import *


router = APIRouter()


@router.post("/", response_model=ResponseModel[PetLine], status_code=status.HTTP_201_CREATED)
def create_pet_line(
    pet_line: PetLineCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    pet_line = pet_line_service.create_pet_line(pet_line)

    return ResponseModel(
        data=pet_line,
        message="pet line created successfully",
        status="success",
    )

@router.get("/", response_model=ResponseModel[list[PetLine]])
def get_pet_lines():
    pet_lines = pet_line_service.get_pet_lines()

    return ResponseModel(
        data=pet_lines,
        message="pet lines retrieved successfully",
        status="success",
    )

@router.get("/{pet_line_id}", response_model=ResponseModel[PetLine])
def get_pet_line(pet_line_id: int):
    pet_line = pet_line_service.get_pet_line(pet_line_id)

    return ResponseModel(
        data=pet_line,
        message="pet line retrieved successfully",
        status="success",
    )

@router.put("/{pet_line_id}", response_model=ResponseModel[PetLine])
def update_pet_line(pet_line_id: int, pet_line: PetLineUpdate):
    pet_line = pet_line_service.update_pet_line(pet_line_id, pet_line)

    return ResponseModel(
        data=pet_line,
        message="pet line updated successfully",
        status="success",
    )

@router.delete("/{pet_line_id}", response_model=ResponseModel[None])
def delete_pet_line(pet_line_id: int):
    pet_line_service.delete_pet_line(pet_line_id)

    return ResponseModel(
        message="pet line deleted successfully",
        status="success",
    )



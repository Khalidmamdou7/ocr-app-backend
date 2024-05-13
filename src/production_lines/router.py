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


@router.post("/", response_model=ResponseModel[ProductionLine], status_code=status.HTTP_201_CREATED)
def create_production_line(
    production_line: ProductionLineCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    production_line = production_line_service.create_production_line(production_line)

    return ResponseModel(
        data=production_line,
        message="Production line created successfully",
        status="success",
    )

@router.get("/", response_model=ResponseModel[list[ProductionLine]])
def get_production_lines():
    production_lines = production_line_service.get_production_lines()

    return ResponseModel(
        data=production_lines,
        message="Production lines retrieved successfully",
        status="success",
    )

@router.get("/{production_line_id}", response_model=ResponseModel[ProductionLine])
def get_production_line(production_line_id: str):
    production_line = production_line_service.get_production_line(production_line_id)

    return ResponseModel(
        data=production_line,
        message="Production line retrieved successfully",
        status="success",
    )

@router.put("/{production_line_id}", response_model=ResponseModel[ProductionLine])
def update_production_line(production_line_id: str, production_line: ProductionLineUpdate):
    production_line = production_line_service.update_production_line(production_line_id, production_line)

    return ResponseModel(
        data=production_line,
        message="Production line updated successfully",
        status="success",
    )

@router.delete("/{production_line_id}", response_model=ResponseModel[None])
def delete_production_line(production_line_id: str):
    production_line_service.delete_production_line(production_line_id)

    return ResponseModel(
        message="Production line deleted successfully",
        status="success",
    )



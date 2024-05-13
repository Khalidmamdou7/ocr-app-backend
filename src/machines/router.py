# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as machine_service
from .models import *


router = APIRouter()


@router.post("/", response_model=ResponseModel[Machine], status_code=status.HTTP_201_CREATED)
def create_machine(
    machine: MachineCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    machine = machine_service.create_machine(machine)

    return ResponseModel(
        data=machine,
        message="machine created successfully",
        status="success",
    )

@router.get("/", response_model=ResponseModel[list[Machine]])
def get_machines(pet_line_id: str | None = None):
    if pet_line_id:
        machines = machine_service.get_machines_by_pet_line_id(pet_line_id)
    else:
        machines = machine_service.get_machines()

    return ResponseModel(
        data=machines,
        message="machines retrieved successfully",
        status="success",
    )

@router.get("/{machine_id}", response_model=ResponseModel[Machine])
def get_machine(machine_id: str):
    machine = machine_service.get_machine(machine_id)

    return ResponseModel(
        data=machine,
        message="machine retrieved successfully",
        status="success",
    )

@router.put("/{machine_id}", response_model=ResponseModel[Machine])
def update_machine(machine_id: str, machine: MachineUpdate):
    machine = machine_service.update_machine(machine_id, machine)

    return ResponseModel(
        data=machine,
        message="machine updated successfully",
        status="success",
    )

@router.delete("/{machine_id}", response_model=ResponseModel[None])
def delete_machine(machine_id: str):
    machine_service.delete_machine(machine_id)

    return ResponseModel(
        message="machine deleted successfully",
        status="success",
    )



# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as counter_service
from .models import *


router = APIRouter()


@router.post("/", response_model=ResponseModel[Counter], status_code=status.HTTP_201_CREATED)
def create_counter(
    counter: CounterCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    counter = counter_service.create_counter(counter)

    return ResponseModel(
        data=counter,
        message="counter created successfully",
        status="success",
    )

@router.get("/", response_model=ResponseModel[list[Counter]])
def get_counters(machine_id: str = None):
    if machine_id:
        counters = counter_service.get_counters_by_machine_id(machine_id)
    else:
        counters = counter_service.get_counters()

    return ResponseModel(
        data=counters,
        message="counters retrieved successfully",
        status="success",
    )

@router.get("/{counter_id}", response_model=ResponseModel[Counter])
def get_counter(counter_id: str):
    counter = counter_service.get_counter(counter_id)

    return ResponseModel(
        data=counter,
        message="counter retrieved successfully",
        status="success",
    )

@router.put("/{counter_id}", response_model=ResponseModel[Counter])
def update_counter(counter_id: str, counter: CounterUpdate):
    counter = counter_service.update_counter(counter_id, counter)

    return ResponseModel(
        data=counter,
        message="counter updated successfully",
        status="success",
    )

@router.delete("/{counter_id}", response_model=ResponseModel[None])
def delete_counter(counter_id: str):
    counter_service.delete_counter(counter_id)

    return ResponseModel(
        message="counter deleted successfully",
        status="success",
    )



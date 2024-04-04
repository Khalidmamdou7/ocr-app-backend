# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum

machines = []

def create_machine(machine: MachineCreate) -> Machine:
    # TODO: Call the DB to create a machine
    machine = MachineInDB(
        id="1",
        name=machine.name,
        pet_line_id=machine.pet_line_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    machines.append(machine)
    return Machine(**machine.dict())

def get_machines() -> list[Machine]:
    machines_in_db = []
    for machine in machines:
        machines_in_db.append(Machine(**machine.dict()))
    return machines_in_db

def get_machines_by_pet_line_id(pet_line_id: str) -> list[Machine]:
    machines_in_db = []
    for machine in machines:
        if machine.pet_line_id == pet_line_id:
            machines_in_db.append(Machine(**machine.dict()))
    return machines_in_db

def get_machine(machine_id: int) -> Machine:
    if machine_id > len(machines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="machine not found")
    return Machine(**machines[machine_id - 1].dict())

def update_machine(machine_id: int, machine: MachineUpdate) -> Machine:
    if machine_id > len(machines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="machine not found")
    machine = machines[machine_id - 1]
    machine.name = machine.name
    machine.pet_line_id = machine.pet_line_id
    machine.updated_at = datetime.now()
    return Machine(**machine.dict())

def delete_machine(machine_id: int):
    machines.pop(machine_id - 1)
# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum
from datetime import datetime
from .schemas import MachinesDB


def create_machine(machine: MachineCreate) -> Machine:
    machine_in_db = MachinesDB().add_machine(MachineInDB(**machine.dict(), created_at=datetime.now(), updated_at=datetime.now()))
    return Machine(**machine_in_db.dict())



def get_machines_by_pet_line_id(pet_line_id: str) -> list[Machine]:
    machines = MachinesDB().get_machines_by_pet_line_id(pet_line_id)
    return [Machine(**machine.dict()) for machine in machines]


def get_machine(machine_id: str) -> Machine:
    machine = MachinesDB().get_machine(machine_id)
    return Machine(**machine.dict())

def get_machines() -> list[Machine]:
    machines = MachinesDB().get_machines()
    return [Machine(**machine.dict()) for machine in machines]

def update_machine(machine_id: str, machine: MachineUpdate) -> Machine:
    machine_in_db = MachinesDB().update_machine(machine_id, machine)
    return Machine(**machine_in_db.dict())

def delete_machine(machine_id: str):
    MachinesDB().delete_machine(machine_id)
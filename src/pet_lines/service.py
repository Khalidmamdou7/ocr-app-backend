# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum
from .schemas import PetLinesDB


def create_pet_line(pet_line: PetLineCreate) -> PetLine:
    pet_line = PetLinesDB().add_pet_line(PetLineInDB(**pet_line.dict()))
    return pet_line


def get_pet_lines() -> list[PetLine]:
    pet_lines = [PetLine(**pet_line_in_db.model_dump()) for pet_line_in_db in PetLinesDB().get_all_pet_lines()]
    return pet_lines

def get_pet_lines_by_production_line_id(production_line_id: str) -> list[PetLine]:
    pet_lines = [PetLine(**pet_line_in_db.model_dump()) for pet_line_in_db in PetLinesDB().get_pet_lines_by_production_line_id(production_line_id)]
    return pet_lines

def get_pet_line(pet_line_id: str) -> PetLine:
    pet_line_in_db = PetLinesDB().get_pet_line(pet_line_id)
    return PetLine(**pet_line_in_db.model_dump())

def update_pet_line(pet_line_id: str, pet_line: PetLineUpdate) -> PetLine:
    
    pet_line_in_db = PetLinesDB().update_pet_line(pet_line_id, pet_line)
    return PetLine(**pet_line_in_db.dict())

def delete_pet_line(pet_line_id: str):
    PetLinesDB().delete_pet_line(pet_line_id)
    return None
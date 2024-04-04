# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum

pet_lines = []

def create_pet_line(pet_line: PetLineCreate) -> PetLine:
    # TODO: Call the DB to create a pet line
    pet_line = PetLineInDB(
        id="1",
        production_line_id=pet_line.production_line_id,
        name=pet_line.name,
        photo_url=pet_line.photo_url,
        flavors=pet_line.flavors,
        sizes=pet_line.sizes,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    pet_lines.append(pet_line)
    return PetLine(**pet_line.dict())

def get_pet_lines() -> list[PetLine]:
    pet_lines_in_db = []
    for pet_line in pet_lines:
        pet_lines_in_db.append(PetLine(**pet_line.dict()))
    return pet_lines_in_db

def get_pet_lines_by_production_line_id(production_line_id: str) -> list[PetLine]:
    pet_lines_in_db = []
    for pet_line in pet_lines:
        if pet_line.production_line_id == production_line_id:
            pet_lines_in_db.append(PetLine(**pet_line.dict()))
    return pet_lines_in_db

def get_pet_line(pet_line_id: int) -> PetLine:
    if pet_line_id > len(pet_lines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pet line not found")
    return PetLine(**pet_lines[pet_line_id - 1].dict())

def update_pet_line(pet_line_id: int, pet_line: PetLineUpdate) -> PetLine:
    if pet_line_id > len(pet_lines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pet line not found")
    pet_line = pet_lines[pet_line_id - 1]
    pet_line.production_line_id = pet_line.production_line_id
    pet_line.name = pet_line.name
    pet_line.photo_url = pet_line.photo_url
    pet_line.flavors = pet_line.flavors
    pet_line.sizes = pet_line.sizes
    pet_line.updated_at = datetime.now()
    return PetLine(**pet_line.dict())

def delete_pet_line(pet_line_id: int):
    pet_lines.pop(pet_line_id - 1)
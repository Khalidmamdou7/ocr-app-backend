# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum

production_lines = []

def create_production_line(production_line: ProductionLineCreate) -> ProductionLine:
    # TODO: Call the DB to create a production line
    production_line = ProductionLineInDB(
        id="1",
        name=production_line.name,
        photo_url=production_line.photo_url,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    production_lines.append(production_line)
    return ProductionLine(**production_line.dict())

def get_production_lines() -> list[ProductionLine]:
    production_lines_in_db = []
    for production_line in production_lines:
        production_lines_in_db.append(ProductionLine(**production_line.dict()))
    return production_lines_in_db

def get_production_line(production_line_id: int) -> ProductionLine:
    if production_line_id > len(production_lines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
    return ProductionLine(**production_lines[production_line_id - 1].dict())

def update_production_line(production_line_id: int, production_line: ProductionLineUpdate) -> ProductionLine:
    if production_line_id > len(production_lines):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
    production_line = production_lines[production_line_id - 1]
    production_line.name = production_line.name
    production_line.photo_url = production_line.photo_url
    production_line.updated_at = datetime.now()
    return ProductionLine(**production_line.dict())

def delete_production_line(production_line_id: int):
    production_lines.pop(production_line_id - 1)
# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum
from .schemas import ProductionLinesDB
from ..utils.utils import db_to_dict, obj_to_dict

production_lines = []

def create_production_line(production_line: ProductionLineCreate) -> ProductionLine:
    # TODO: Call the DB to create a production line
    production_line = ProductionLinesDB().add_production_line(ProductionLineInDB(**production_line.dict()))
    
    return production_line

def get_production_lines() -> list[ProductionLine]:
    
    production_lines = [ProductionLine(**production_line_in_db.model_dump()) for production_line_in_db in ProductionLinesDB().get_all_production_lines()]
    return production_lines

def get_production_line(production_line_id: int) -> ProductionLine:
    production_line_in_db = ProductionLinesDB().get_production_line(production_line_id)
    return ProductionLine(**production_line_in_db.model_dump())

def update_production_line(production_line_id: int, production_line: ProductionLineUpdate) -> ProductionLine:
    
    production_line_in_db = ProductionLinesDB().update_production_line(production_line_id, production_line)
    return ProductionLine(**production_line_in_db.dict())

def delete_production_line(production_line_id: int):
    ProductionLinesDB().delete_production_line(production_line_id)
    return None
# schemas.py
# DB logic goes here

from fastapi import HTTPException, status
from .models import PetLineInDB, PetLine, PetLineCreate, PetLineUpdate
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from ..utils.utils import db_to_dict
from datetime import datetime



class PetLinesDB():

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('pet_lines')

    def add_pet_line(self, pet_line: PetLineInDB) -> PetLineInDB:
        """
        Add a new pet line to the database.

        Args:
            pet_line (PetLineInDB): the pet line to be added

        Returns:
            PetLine: the pet line that was added
        
        Raises:
            HTTPException: if the pet line already exists, or data validation fails
        """
        try:
            pet_line_in_db = pet_line.model_dump()
            # Check if the production line exists
            production_line = self.db.get_collection('production_lines').find_one({"_id": ObjectId(pet_line_in_db['production_line_id'])})
            if production_line is None:
                raise HTTPException(status_code=400, detail="Production line not found")
            pet_line_in_db["_id"] = self.collection.insert_one(pet_line_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Pet line already exists with the same " + duplicate_key)
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        
        return PetLine(**db_to_dict(pet_line_in_db))
    
    def get_pet_line(self, pet_line_id: str) -> PetLineInDB:
        """
        Get a pet line from the database.

        Args:
            pet_line_id (str): the identifier of the pet line to be retrieved

        Returns:
            PetLineInDB: the pet line that was retrieved
        
        """
        pet_line = self.collection.find_one({"_id": ObjectId(pet_line_id)})
        if pet_line is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet line not found")
        pet_line = PetLineInDB(**db_to_dict(pet_line))
        return pet_line
    
    def get_pet_lines_by_production_line_id(self, production_line_id: str) -> list[PetLineInDB]:
        """
        Get all pet lines from the database that belong to a specific production line.

        Args:
            production_line_id (str): the identifier of the production line

        Returns:
            list[PetLineInDB]: the pet lines that were retrieved
        
        """
        try:
            pet_lines = self.collection.find({"production_line_id": production_line_id})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        pet_lines = [PetLineInDB(**db_to_dict(pet_line)) for pet_line in pet_lines]
        return pet_lines
    
    def get_all_pet_lines(self) -> list[PetLineInDB]:
        """
        Get all pet lines from the database.

        Returns:
            list[PetLineInDB]: the pet lines that were retrieved
        
        """
        pet_lines = self.collection.find()
        pet_lines = [PetLineInDB(**db_to_dict(pet_line)) for pet_line in pet_lines]
        return pet_lines
    
    def update_pet_line(self, pet_line_id: str, pet_line: PetLineUpdate) -> PetLineInDB:
        """
        Update a pet line in the database.

        Args:
            pet_line_id (str): the identifier of the pet line to be updated
            pet_line (PetLineUpdate): the pet line data to be updated

        Returns:
            PetLineInDB: the pet line that was updated
        
        """
        pet_line_in_db = self.get_pet_line(pet_line_id).model_dump()
        pet_line_in_db.update(pet_line.dict(exclude_unset=True))
        pet_line_in_db['updated_at'] = datetime.utcnow()
        # Check if the production line exists
        try:
            production_line = self.db.get_collection('production_lines').find_one({"_id": ObjectId(pet_line_in_db['production_line_id'])})
            if production_line is None:
                raise HTTPException(status_code=400, detail="Production line not found")
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        self.collection.update_one({"_id": ObjectId(pet_line_id)}, {"$set": pet_line_in_db})
        return PetLineInDB(**db_to_dict(pet_line_in_db))
    
    def delete_pet_line(self, pet_line_id: str):
        """
        Delete a pet line from the database.

        Args:
            pet_line_id (str): the identifier of the pet line to be deleted

        Returns:
            None
        
        """
        result = self.collection.delete_one({"_id": ObjectId(pet_line_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet line not found")
        return None

# schemas.py
# DB logic goes here

from fastapi import HTTPException, status
from .models import ProductionLineInDB, ProductionLine, ProductionLineCreate, ProductionLineUpdate
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from ..utils.utils import db_to_dict
from datetime import datetime

class ProductionLinesDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('production_lines')
    
    def add_production_line(self, production_line: ProductionLineInDB) -> ProductionLine:
        """
        Add a new production line to the database.

        Args:
            production_line (ProductionLineInDB): the production line to be added

        Returns:
            ProductionLine: the production line that was added
        
        Raises:
            HTTPException: if the production line already exists, or data validation fails
        """
        try:
            production_line_in_db = production_line.model_dump()
            production_line_in_db["_id"] = self.collection.insert_one(production_line_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Production line already exists with the same " + duplicate_key)
        
        return ProductionLine(**db_to_dict(production_line_in_db))
    
    def get_production_line(self, production_line_id: str) -> ProductionLineInDB:
        """
        Get a production line from the database.

        Args:
            production_line_id (str): the identifier of the production line to be retrieved

        Returns:
            ProductionLineInDB: the production line that was retrieved
        
        """
        production_line = self.collection.find_one({"_id": ObjectId(production_line_id)})
        if production_line is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
        production_line = ProductionLineInDB(**db_to_dict(production_line))
        return production_line
    
    def get_all_production_lines(self) -> list[ProductionLineInDB]:
        """
        Get all production lines from the database.

        Returns:
            list[ProductionLineInDB]: the production lines that were retrieved
        
        """
        production_lines = self.collection.find()
        production_lines = [ProductionLineInDB(**db_to_dict(production_line)) for production_line in production_lines]
        return production_lines
    

    def update_production_line(self, production_line_id: str, production_line: ProductionLineUpdate) -> ProductionLineInDB:
        """
        Update a production line in the database.

        Args:
            production_line_id (str): the identifier of the production line to be updated
            production_line (ProductionLineUpdate): the updated production line

        Returns:
            ProductionLineInDB: the production line that was updated
        
        """
        production_line = production_line.dict(exclude_unset=True)
        updated_at = datetime.now()
        production_line['updated_at'] = updated_at
        result = self.collection.update_one({"_id": ObjectId(production_line_id)}, {"$set": production_line})
        if result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
        production_line = self.get_production_line(production_line_id)
        return production_line
    
    def delete_production_line(self, production_line_id: str):
        """
        Delete a production line from the database.

        Args:
            production_line_id (str): the identifier of the production line to be deleted
        
        """
        result = self.collection.delete_one({"_id": ObjectId(production_line_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
        return
    
    def delete_all_production_lines(self):
        """
        Delete all production lines from the database.
        
        """
        self.collection.delete_many({})
        return
    
    def get_production_line_by_name(self, name: str) -> ProductionLineInDB:
        """
        Get a production line from the database by name.

        Args:
            name (str): the name of the production line to be retrieved

        Returns:
            ProductionLineInDB: the production line that was retrieved
        
        """
        production_line = self.collection.find_one({"name": name})
        if production_line is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production line not found")
        production_line = ProductionLineInDB(**db_to_dict(production_line))
        return production_line
    
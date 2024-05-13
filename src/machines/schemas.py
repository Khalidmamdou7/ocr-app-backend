# schemas.py
# DB logic goes here

from fastapi import HTTPException, status
from .models import MachineInDB, Machine, MachineCreate, MachineUpdate
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from ..utils.utils import db_to_dict
from datetime import datetime



class MachinesDB():

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('machines')

    def add_machine(self, machine: MachineInDB) -> MachineInDB:
        """
        Add a new machine to the database.

        Args:
            machine (MachineInDB): the machine to be added

        Returns:
            Machine: the machine that was added
        
        Raises:
            HTTPException: if the machine already exists, or data validation fails
        """
        try:
            machine_in_db = machine.model_dump()
            # Check if the production line exists
            pet_line = self.db.get_collection('pet_lines').find_one({"_id": ObjectId(machine_in_db['pet_line_id'])})
            if pet_line is None:
                raise HTTPException(status_code=400, detail="Production line not found")
            machine_in_db["_id"] = self.collection.insert_one(machine_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Machine already exists with the same " + duplicate_key)
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        
        return Machine(**db_to_dict(machine_in_db))
    
    def get_machine(self, machine_id: str) -> MachineInDB:
        """
        Get a machine from the database.

        Args:
            machine_id (str): the identifier of the machine to be retrieved

        Returns:
            MachineInDB: the machine that was retrieved
        
        """
        try:
            machine = self.collection.find_one({"_id": ObjectId(machine_id)})
            if machine is None:
                raise HTTPException(status_code=404, detail="Machine not found")
            return MachineInDB(**db_to_dict(machine))
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid machine id")
        
    def get_machines_by_pet_line_id(self, pet_line_id: str) -> list[MachineInDB]:
        """
        Get all machines from the database that belong to a specific pet line.
        """
        machines = self.collection.find({"pet_line_id": pet_line_id})
        return [MachineInDB(**db_to_dict(machine)) for machine in machines]
    
    def update_machine(self, machine_id: str, machine: MachineUpdate) -> MachineInDB:
        """
        Update a machine in the database.
        """
        machine_in_db = machine.model_dump()
        machine_in_db['updated_at'] = datetime.now()
        try:
            pet_line = self.db.get_collection('pet_lines').find_one({"_id": ObjectId(machine_in_db['pet_line_id'])})
            if pet_line is None:
                raise HTTPException(status_code=400, detail="Production line not found")
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        self.collection.update_one({"_id": ObjectId(machine_id)}, {"$set": machine_in_db})
        return self.get_machine(machine_id)
    
    def delete_machine(self, machine_id: str) -> None:
        """
        Delete a machine from the database.
        """
        
        try:
            self.collection.delete_one({"_id": ObjectId(machine_id)})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid machine id")
        
    
    


# schemas.py
# DB logic goes here


from fastapi import HTTPException, status
from .models import CounterInDB, Counter, CounterCreate, CounterUpdate
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from ..utils.utils import db_to_dict
from datetime import datetime



class CountersDB():

    
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('counters')

    def add_counter(self, counter: CounterInDB) -> CounterInDB:
        """
        Add a new counter to the database.

        Args:
            counter (CounterInDB): the counter to be added

        Returns:
            Counter: the counter that was added
        
        Raises:
            HTTPException: if the counter already exists, or data validation fails
        """
        try:
            counter_in_db = counter.model_dump()
            # Check if the machine exists
            machine = self.db.get_collection('machines').find_one({"_id": ObjectId(counter_in_db['machine_id'])})
            if machine is None:
                raise HTTPException(status_code=400, detail="Machine not found")
            counter_in_db["_id"] = self.collection.insert_one(counter_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Counter already exists with the same " + duplicate_key)
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid production line id")
        
        return Counter(**db_to_dict(counter_in_db))
    
    def get_counter(self, counter_id: str) -> CounterInDB:
        """
        Get a counter from the database.

        Args:
            counter_id (str): the identifier of the counter to be retrieved

        Returns:
            CounterInDB: the counter that was retrieved
        
        """
        try:
            counter = self.collection.find_one({"_id": ObjectId(counter_id)})
            if counter is None:
                raise HTTPException(status_code=400, detail="Counter not found")
            return CounterInDB(**db_to_dict(counter))
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid counter id")
        
    def get_counters(self) -> list[CounterInDB]:
        """
        Get all counters from the database.

        Returns:
            list[CounterInDB]: the counters that were retrieved
        
        """
        counters = self.collection.find()
        return [CounterInDB(**db_to_dict(counter)) for counter in counters]
        
    def get_counters_by_machine_id(self, machine_id: str) -> list[CounterInDB]:
        """
        Get all counters from a machine.

        Args:
            machine_id (str): the identifier of the machine

        Returns:
            list[CounterInDB]: the counters that were retrieved
        
        """
        try:
            counters = self.collection.find({"machine_id": ObjectId(machine_id)})
            return [CounterInDB(**db_to_dict(counter)) for counter in counters]
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid machine id")
        
    def update_counter(self, counter_id: str, counter: CounterUpdate) -> CounterInDB:
        """
        Update a counter in the database.

        Args:
            counter_id (str): the identifier of the counter to be updated
            counter (CounterUpdate): the new data for the counter

        Returns:
            CounterInDB: the counter that was updated
        
        """
        try:
            counter_in_db = counter.model_dump()
            counter_in_db['updated_at'] = datetime.now()
            # Check if the machine exists
            try:
                machine = self.db.get_collection('machines').find_one({"_id": ObjectId(counter_in_db['machine_id'])})
                if machine is None:
                    raise HTTPException(status_code=400, detail="Machine not found")
            except InvalidId as e:
                raise HTTPException(status_code=400, detail="Invalid machine id")
            self.collection.update_one({"_id": ObjectId(counter_id)}, {"$set": counter_in_db})
            return CounterInDB(**db_to_dict(counter_in_db))
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid counter id")
        
    def delete_counter(self, counter_id: str) -> None:
        """
        Delete a counter from the database.

        Args:
            counter_id (str): the identifier of the counter to be deleted
        
        """
        try:
            self.collection.delete_one({"_id": ObjectId(counter_id)})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid counter id")
        


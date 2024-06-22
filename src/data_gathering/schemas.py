# schemas.py
# DB logic goes here



from fastapi import HTTPException, status
from .models import *
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from ..utils.utils import db_to_dict
from datetime import datetime


class OcrModelDB():

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('ocr_models')

    def add_ocr_model(self, ocr_model: OcrModelInDB) -> OcrModel:
        """
        Add a new ocr_model to the database.

        Args:
            ocr_model (OcrModelInDB): the ocr_model to be added

        Returns:
            OcrModel: the ocr_model that was added
        
        Raises:
            HTTPException: if the ocr_model already exists, or data validation fails
        """
        try:
            ocr_model_in_db = ocr_model.model_dump()
            # Check if the counter exists
            counter = self.db.get_collection('counters').find_one({"_id": ObjectId(ocr_model_in_db['counter_id'])})
            if counter is None:
                raise HTTPException(status_code=400, detail="counter not found")
            ocr_model_in_db["_id"] = self.collection.insert_one(ocr_model_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="OcrModel already exists with the same " + duplicate_key)
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid counter id")
        
        return OcrModel(**db_to_dict(ocr_model_in_db))
    
    def get_ocr_model(self, ocr_model_id: str) -> OcrModelInDB:
        """
        Get a ocr_model from the database.

        Args:
            ocr_model_id (str): the identifier of the ocr_model to be retrieved

        Returns:
            OcrModelInDB: the ocr_model that was retrieved
        
        """
        try:
            ocr_model = self.collection.find_one({"_id": ObjectId(ocr_model_id)})
            if ocr_model is None:
                raise HTTPException(status_code=404, detail="OcrModel not found")
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid ocr_model id")
        return OcrModelInDB(**db_to_dict(ocr_model))
    
    def get_ocr_models(self) -> list[OcrModel]:
        """
        Get all ocr_models from the database.

        Returns:
            list[OcrModelInDB]: the ocr_models that were retrieved
        
        """
        ocr_models = self.collection.find()
        return [OcrModelInDB(**db_to_dict(ocr_model)) for ocr_model in ocr_models]
    
    def get_ocr_models_by_counter_id(self, counter_id: str) -> list[OcrModelInDB]:
        """
        Get all ocr_models from the database.

        Returns:
            list[OcrModelInDB]: the ocr_models that were retrieved
        
        """
        ocr_models = self.collection.find({"counter_id": counter_id})
        return [OcrModelInDB(**db_to_dict(ocr_model)) for ocr_model in ocr_models]
    
    def update_ocr_model(self, ocr_model_id: str, ocr_model: OcrModelUpdate) -> OcrModelInDB:
        """
        Update a ocr_model in the database.

        Args:
            ocr_model_id (str): the identifier of the ocr_model to be updated
            ocr_model (OcrModelUpdate): the updated ocr_model

        Returns:
            OcrModelInDB: the ocr_model that was updated
        
        Raises:
            HTTPException: if the ocr_model does not exist, or data validation fails
        """
        try:
            ocr_model_in_db = ocr_model.model_dump()
            # Check if the counter exists
            counter = self.db.get_collection('counters').find_one({"_id": ObjectId(ocr_model_in_db['counter_id'])})
            if counter is None:
                raise HTTPException(status_code=400, detail="counter not found")
            self.collection.update_one({"_id": ObjectId(ocr_model_id)}, {"$set": ocr_model_in_db})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid ocr_model id")
        
        return self.get_ocr_model(ocr_model_id)
    
    def delete_ocr_model(self, ocr_model_id: str):
        """
        Delete a ocr_model from the database.

        Args:
            ocr_model_id (str): the identifier of the ocr_model to be deleted
        
        Raises:
            HTTPException: if the ocr_model does not exist
        """
        try:
            model = self.get_ocr_model(ocr_model_id)
            self.collection.delete_one({"_id": ObjectId(ocr_model_id)})
            return model
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid ocr_model id")
        except Exception as e:
            raise HTTPException(status_code=404, detail="OcrModel not found")
        

class DataDB:

    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('data')

    def add_data(self, data: DataInDB) -> DataResponse:
        """
        Add a new data to the database.

        Args:
            data (DataInDB): the data to be added

        Returns:
            DataInDB: the data that was added
        
        Raises:
            HTTPException: if the data already exists, or data validation fails
        """
        try:
            data_in_db = data.model_dump()
           
            # Check if the counter exists
            counter = self.db.get_collection('counters').find_one({"_id": ObjectId(data_in_db['counter_id'])})
            if counter is None:
                raise HTTPException(status_code=400, detail="counter not found")
            # Check if the uploader exists
            uploader = self.db.get_collection('users').find_one({"username": data_in_db['uploader_username']})
            if uploader is None:
                raise HTTPException(status_code=400, detail="uploader not found")
            data_in_db["_id"] = self.collection.insert_one(data_in_db).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="Data already exists with the same " + duplicate_key)
        
        
        return DataResponse(**db_to_dict(data_in_db))
    
    def get_data(self, data_id: str) -> DataResponse:
        """
        Get a data from the database.

        Args:
            data_id (str): the identifier of the data to be retrieved

        Returns:
            DataInDB: the data that was retrieved
        
        """
        try:
            data = self.collection.find_one({"_id": ObjectId(data_id)})
            if data is None:
                raise HTTPException(status_code=404, detail="Data not found")
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid data id")
        return DataResponse(**db_to_dict(data))
    
    def get_data_by_ocr_model_id(self, ocr_model_id: str) -> list[DataInDB]:
        """
        Get all data from the database.

        Returns:
            list[DataInDB]: the data that were retrieved
        
        """
        data = self.collection.find({"ocr_model_id": ocr_model_id})
        return [DataInDB(**db_to_dict(data)) for data in data]
    
    def get_data_by_counter_id(self, counter_id: str) -> list[DataInDB]:
        """
        Get all data from the database.

        Returns:
            list[DataInDB]: the data that were retrieved
        
        """
        data = self.collection.find({"counter_id": counter_id})
        return [DataInDB(**db_to_dict(data)) for data in data]
    
    def get_data_by_date(self, date: datetime) -> list[DataInDB]:
        """
        Get all data from the database.

        Returns:
            list[DataInDB]: the data that were retrieved
        
        """
        data = self.collection.find({"date": date})
        return [DataInDB(**db_to_dict(data)) for data in data]
    
    def get_data_by_uploader_id(self, uploader_username: str) -> list[DataInDB]:
        """
        Get all data from the database.

        Returns:
            list[DataInDB]: the data that were retrieved
        
        """
        data = self.collection.find({"uploader_username": uploader_username})
        return [DataInDB(**db_to_dict(data)) for data in data]
    
    def update_data(self, data_id: str, data: DataUpdate) -> DataInDB:
        """
        Update a data in the database.

        Args:
            data_id (str): the identifier of the data to be updated
            data (DataUpdate): the updated data

        Returns:
            DataInDB: the data that was updated
        
        Raises:
            HTTPException: if the data does not exist, or data validation fails
        """
        try:
            data_in_db = data.model_dump()
            # Check if the counter exists
            counter = self.db.get_collection('counters').find_one({"_id": ObjectId(data_in_db['counter_id'])})
            if counter is None:
                raise HTTPException(status_code=400, detail="counter not found")
            # Check if the uploader exists
            uploader = self.db.get_collection('users').find_one({"username": data_in_db['uploader_username']})
            if uploader is None:
                raise HTTPException(status_code=400, detail="uploader not found")
            self.collection.update_one({"_id": ObjectId(data_id)}, {"$set": data_in_db})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid data id")
        
        return DataInDB(**db_to_dict(data_in_db))
    
    def delete_data(self, data_id: str):
        """
        Delete a data from the database.

        Args:
            data_id (str): the identifier of the data to be deleted
        
        Raises:
            HTTPException: if the data does not exist
        """
        try:
            self.collection.delete_one({"_id": ObjectId(data_id)})
        except InvalidId as e:
            raise HTTPException(status_code=400, detail="Invalid data id")
        except Exception as e:
            raise HTTPException(status_code=404, detail="Data not found")



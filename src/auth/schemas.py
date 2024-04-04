# schemas.py
# DB logic goes here

# for db

from fastapi import HTTPException, status
from .models import UserInDB, UserCreateResponse, RoleEnum, UserResponse
from ..database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from ..utils.utils import db_to_dict

class UsersDB():
    def __init__(self):
        self.db = Database()
        self.collection = self.db.get_collection('users')
    

    def add_user(self, user: UserInDB):
        """
        Add a new user to the database.

        Args:
            user (UserInDB): the user to be added

        Returns:
            UserCreateResponse: the user that was added
        
        Raises:
            HTTPException: if the user already exists, or data validation fails
        """
        try:
            inserted_id = self.collection.insert_one(user.model_dump()).inserted_id
        except DuplicateKeyError as e:
            duplicate_key = list(e.details['keyPattern'].keys())[0]
            raise HTTPException(status_code=400, detail="User already exists with the same " + duplicate_key)
        

        return UserCreateResponse(**user.model_dump())
    
    def get_user(self, identifier: str) -> UserInDB:
        """
        Get a user from the database.

        Args:
            identifier (str): the identifier of the user to be retrieved

        Returns:
            UserInDB: the user that was retrieved
        
        """
        user = self.collection.find_one({"$or": [{"email": identifier}, {"username": identifier}, {"mobile": identifier}]})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = UserInDB(**db_to_dict(user))
        return user
    
    def get_user_by_id(self, user_id: str):
        """
        Get a user from the database.

        Args:
            user_id (str): the id of the user to be retrieved

        Returns:
            UserInDB: the user that was retrieved
        
        """
        try:
            user_id = ObjectId(user_id)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        user = self.collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return UserInDB(**db_to_dict(user))
    
    def update_user(self, user: UserInDB):
        """
        Update a user in the database.

        Args:
            user (UserInDB): the user to be updated

        Returns:
            UserInDB: the user that was updated
        
        Raises:
            HTTPException: if the user does not exist
        """

        if not self.collection.find_one({"username": user.username}):
            raise HTTPException(status_code=404, detail="User not found")
        
        self.collection.update_one({"username": user.username}, {"$set": user.model_dump()})
        return user

    def get_admin_user(self) -> UserInDB or None:
        """
        Get the admin user from the database.

        Returns:
            UserInDB: the admin user
        """
        admin_user = self.collection.find_one({"role": RoleEnum.ADMIN})
        if admin_user is None:
            return None
        return UserInDB(**db_to_dict(admin_user))
    
    
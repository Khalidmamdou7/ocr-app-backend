# Database connection and configuration


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException, status
from .config import APP_SETTINGS


class Database:
    """
    A singleton class that initializes a MongoDB connection and provides a method to get a collection.

    Usage:
    from database import Database
    db = Database()
    collection = db.get_collection('collection_name')

    raises:
        HTTPException: if the db connection fails
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialize_connection()
        return cls._instance

    def initialize_connection(self):

        self.client = MongoClient(APP_SETTINGS.MONGODB_URI, server_api=ServerApi('1'))
        self.db = self.client[APP_SETTINGS.MONGODB_DB_NAME]
        try:
            # Ping the server to see if the connection is successful
            self.client.admin.command('ping')
            print('Connected to MongoDB')
            self.create_indexes()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection failed")


    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def create_indexes(self):

        self.db.users.create_index('username', unique=True)
        self.db.users.create_index('email', unique=True)
        self.db.users.create_index('mobile', unique=True)


        print('Created indexes successfully')

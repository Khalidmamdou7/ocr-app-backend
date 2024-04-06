# utils.py
# Non-business logic related utility functions go here (e.g. hashing, etc.)
# Helper functions that are used in the service layer go here

import cloudinary
import cloudinary.uploader
import json
from ..config import APP_SETTINGS
import os

cloudinary.config( 
  cloud_name = APP_SETTINGS.CLOUDINARY_CLOUD_NAME,
  api_key = APP_SETTINGS.CLOUDINARY_API_KEY,
  api_secret = APP_SETTINGS.CLOUDINARY_API_SECRET.get_secret_value() 
)

def upload_image_to_cloudinary(file_path: str):
    upload_result = cloudinary.uploader.upload(file_path)
    print("File uploaded to cloudinary successfully: ", upload_result["secure_url"])
    delete_file(file_path)
    return upload_result["secure_url"]

def delete_file(file_path: str):
    os.remove(file_path)
    print("File deleted successfully: ", file_path)

    

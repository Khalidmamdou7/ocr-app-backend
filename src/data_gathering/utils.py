# utils.py
# Non-business logic related utility functions go here (e.g. hashing, etc.)
# Helper functions that are used in the service layer go here

import cloudinary
import cloudinary.uploader
import json
from ..config import APP_SETTINGS
import os
from ..utils.gsheet import get_gsheet_data, write_gsheet_data
from .models import DataInDB
import datetime

gsheet_strcuture = {
   "gsheet_id": "1oXF7eSnqyrFa6sigLoA4vE3Ndb1o9l3goESes5vvODo",
   "counters": {
      "1": {
         "sheet_name": "khaled-test",
         "firstcolumn_letter": "A",
         "lastcolumn_letter": "P",
         "timestamp_column": 0,
         "username_column": 1,
         "img_link_column": 2,
         "date_column": 3,
         "shift_column": 4,
         "co_column": 5,
         "flavour_column": 6,
         "size_column": 7,
         "headers_columns": {
            "Total Production": 8,
            "Good Production": 9,
            "Rejection": 10,
            "Neck Finish": 11,
            "Ovality": 12,
            "Foreign Container": 13,
            "Coloured Container": 14,
            "Rejection signal": 15
         }
      }
   }
}

cloudinary.config( 
  cloud_name = APP_SETTINGS.CLOUDINARY_CLOUD_NAME,
  api_key = APP_SETTINGS.CLOUDINARY_API_KEY,
  api_secret = APP_SETTINGS.CLOUDINARY_API_SECRET.get_secret_value() 
)

def upload_image_to_cloudinary(file_path: str):
    upload_result = cloudinary.uploader.upload(file_path)
    print("File uploaded to cloudinary successfully: ", upload_result["secure_url"])
    # delete_file(file_path)
    return upload_result["secure_url"]

def delete_file(file_path: str):
    os.remove(file_path)
    print("File deleted successfully: ", file_path)

def write_data_entry_to_gsheet(data_entry_obj: DataInDB):
    gsheet_id = gsheet_strcuture["gsheet_id"]
    # TODO: Use this after constructing the gsheet structure for each counter
    # counter_gsheet_strcuture = gsheet_strcuture["counters"][data_entry_obj.counter_id]
    counter_gsheet_strcuture = gsheet_strcuture["counters"]['1']

    sheet_name = counter_gsheet_strcuture["sheet_name"]
    firstcolumn_letter = counter_gsheet_strcuture["firstcolumn_letter"]
    lastcolumn_letter = counter_gsheet_strcuture["lastcolumn_letter"]

 
    headers_columns = counter_gsheet_strcuture["headers_columns"]
    date = data_entry_obj.created_at.date().isoformat()
    shift = get_shift_from_timestamp(data_entry_obj.created_at)
    # TODO: Change the default value of co
    co = "Yes"
    col_values_dict = {
       counter_gsheet_strcuture["timestamp_column"]: data_entry_obj.created_at.isoformat(),
       counter_gsheet_strcuture["username_column"]: data_entry_obj.uploader_username,
       counter_gsheet_strcuture["img_link_column"]: data_entry_obj.file_url,
       counter_gsheet_strcuture["date_column"]: date,
       counter_gsheet_strcuture["shift_column"]: shift,
       counter_gsheet_strcuture["co_column"]: co,
       counter_gsheet_strcuture["flavour_column"]: data_entry_obj.flavor,
       counter_gsheet_strcuture["size_column"]: data_entry_obj.size
   }

    for header, column in headers_columns.items():
       col_values_dict[column] = data_entry_obj.collected_info_values.get(header, 0)
   
    # sort col_values_dict by column number
    col_values_dict = dict(sorted(col_values_dict.items(), key=lambda item: item[0]))
    # convert data to list sorted by column number starting from the smallest and if there is a missing column, it will be filled with None
    sorted_values_list = [col_values_dict.get(i, None) for i in range(len(col_values_dict))]
    write_gsheet_data(gsheet_id, sheet_name, firstcolumn_letter, lastcolumn_letter, [sorted_values_list])



def get_shift_from_timestamp(timestamp: datetime.datetime) -> str:
    if timestamp.hour < 12:
        return 1
    elif timestamp.hour < 20:
        return 2
    else:
        return 3
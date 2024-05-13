# service.py
# Module specific business logic goes here

# service.py
# Module specific business logic goes here

from typing import Annotated

from fastapi import Depends, HTTPException, status, UploadFile, File, BackgroundTasks

from .models import *
from ..auth.schemas import UsersDB
from ..auth.models import User, RoleEnum

from .utils import upload_image_to_cloudinary, write_data_entry_to_gsheet
from ..utils.ocr_model import get_digits_from_image, add_model, get_model, delete_model
from datetime import datetime
from .schemas import DataDB, OcrModelDB

import os



async def upload_ocr_model(
        ocr_model_file: File,
        counter_id: str,
        collected_info: list[str],
        background_tasks: BackgroundTasks,
) -> OcrModel:
    OCR_MODEL_DB = OcrModelDB()
    ocr_model: OcrModel = OCR_MODEL_DB.add_ocr_model(OcrModelInDB(
        counter_id=counter_id,
        file_name=ocr_model_file.filename,
        collected_info=collected_info,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        file_path=None,
    ))


    model_id = ocr_model.id
    model_name = f"model_{model_id}_counter_{counter_id}_{ocr_model_file.filename}"
    
    # store the file in the server in a folder called 'ocr-models'
    if not os.path.exists('ocr-models'):
        os.makedirs('ocr-models')
    with open(f'ocr-models/{model_name}', 'wb') as f:
        f.write(ocr_model_file.file.read())
    
    # background task to load the model
    background_tasks.add_task(add_model, model_name)

    ocr_model.file_name = model_name
    ocr_model.file_path = f'ocr-models/{model_name}'
    background_tasks.add_task(OCR_MODEL_DB.update_ocr_model, model_id, OcrModelUpdate(**ocr_model.dict()))
    
    return OcrModel(**ocr_model.dict())

def get_ocr_models_ids(counter_id: str | None) -> list[OcrModel]:
    if counter_id is None:
        ocr_models = OcrModelDB().get_ocr_models()
    else:
        ocr_models_in_db = OcrModelDB().get_ocr_models_by_counter_id(counter_id)
        ocr_models = [OcrModel(**model.dict()) for model in ocr_models_in_db]

    return ocr_models

async def get_ocr_model(model_id: str) -> OcrModel | str:
    ocr_model = OcrModelDB().get_ocr_model(model_id)
    return OcrModel(**ocr_model.dict())

def update_ocr_model(
        background_tasks: BackgroundTasks,
        model_id: str,
        counter_id: str,
        collected_info: list[str],
        model_file: UploadFile | None,
) -> OcrModel:
    ocr_model = OcrModelDB().update_ocr_model(
        model_id,
        OcrModelUpdate(
            counter_id=counter_id,
            collected_info=collected_info,
            updated_at=datetime.now(),
        )
    )
    if model_file:
        model_name = f"model_{model_id}_counter_{counter_id}_{model_file.filename}"
        # store the file in the server in a folder called 'ocr-models'
        if not os.path.exists('ocr-models'):
            os.makedirs('ocr-models')
        with open(f'ocr-models/{model_name}', 'wb') as f:
            f.write(model_file.file.read())
        ocr_model.file_name = model_file.filename
        ocr_model.file_path = f'ocr-models/{model_name}'
        background_tasks.add_task(add_model, model_name)
    return OcrModel(**ocr_model.dict())

def delete_ocr_model(model_id: str):
    model = OcrModelDB().delete_ocr_model(model_id)
    delete_model(model.file_name)
    

async def upload_data(
        data_file: UploadFile,
        counter_id: str,
        flavor: str,
        size: str,
        collected_info_values: object,
        current_user: User,
        background_tasks: BackgroundTasks,
) -> DataResponse:
        
        # store the file in the server in a folder called 'data'
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(f'data/{data_file.filename}', 'wb') as f:
            f.write(data_file.file.read())
            file_path = f'data/{data_file.filename}'
        
        ocr_models = OcrModelDB().get_ocr_models_by_counter_id(counter_id)
        if len(ocr_models) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No OCR models found for this counter")
        ocr_model = ocr_models[0]
        
        model_name = ocr_model.file_name
        results = get_digits_from_image(file_path, model_name)
        print(results)

        
        data_obj = DataDB().add_data(DataInDB(
            counter_id=counter_id,
            ocr_model_id=ocr_model.id,
            flavor=flavor,
            size=size,
            collected_info_values=results,
            uploader_username=current_user.username,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            file_url=None,
        ))
        background_tasks.add_task(upload_image_and_write_data_to_gsheet, file_path, data_obj)
        return DataResponse(**data_obj.dict())

def get_data_ids(counter_id: str | None, flavor: str | None, size: str | None, uploader_username: str | None, start_date: str | None, end_date: str | None) -> list[DataResponse]:
    if counter_id:
        data_in_db = DataDB().get_data_by_counter_id(counter_id)
    elif uploader_username:
        data_in_db = DataDB().get_data_by_uploader_id(uploader_username)
    # TODO: add more filters
    data = [DataResponse(**data_obj.dict()) for data_obj in data_in_db]
    return data

def get_data(data_id: str) -> DataResponse:
    data = DataDB().get_data(data_id)
    return DataResponse(**data.dict())

def update_data(
        data_id: str,
        counter_id: str,
        flavor: str,
        size: str,
        collected_info_values: object,
        data_file: UploadFile | None,
) -> DataResponse:
    data = DataDB().update_data(
        data_id,
        DataUpdate(
            counter_id=counter_id,
            flavor=flavor,
            size=size,
            collected_info_values=collected_info_values,
            updated_at=datetime.now(),
        )
    )
    if data_file:
        # store the file in the server in a folder called 'data'
        if not os.path.exists('data'):
            os.makedirs('data')
        with open(f'data/{data_file.filename}', 'wb') as f:
            f.write(data_file.file.read())
            file_path = f'data/{data_file.filename}'
        data.file_url = upload_image_to_cloudinary(file_path)
    return DataResponse(**data.dict())

def delete_data(data_id: str):
    DataDB().delete_data(data_id)


def upload_image_and_write_data_to_gsheet(
        file_path: str,
        data_entry_obj: DataInDB,
):
    uploaded_image_url = upload_image_to_cloudinary(file_path)
    data_entry_obj.file_url = uploaded_image_url
    write_data_entry_to_gsheet(data_entry_obj)



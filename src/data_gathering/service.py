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
# from ..utils.ocr_model import get_digits_from_image

import os

ocr_models = []
data = []

async def upload_ocr_model(
        ocr_model_file: File,
        counter_id: str,
        collected_info: list[str],
) -> OcrModelResponse:
    print(type(ocr_model_file))
    
    # store the file in the server in a folder called 'ocr-models'
    if not os.path.exists('ocr-models'):
        os.makedirs('ocr-models')
    with open(f'ocr-models/{ocr_model_file.filename}', 'wb') as f:
        f.write(ocr_model_file.file.read())

    # create a model object
    ocr_model = OcrModelInDB(
        _id=str(len(ocr_models) + 1),
        counter_id=counter_id,
        collected_info=collected_info,
        file_name=ocr_model_file.filename,
        file_path=f'ocr-models/{ocr_model_file.filename}',
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    print(ocr_model.dict())
    ocr_models.append(ocr_model)
    return OcrModelResponse(**ocr_model.dict())

def get_ocr_models_ids(counter_id: str | None) -> list[OcrModelResponse]:
    models_in_db = []
    for model in ocr_models:
        if counter_id is None or model.counter_id == counter_id:
            models_in_db.append(OcrModelResponse(**model.dict()))
    return models_in_db

async def get_ocr_model(model_id: str, file: bool = False) -> OcrModelResponse | str:
    model_id = int(model_id)
    if model_id > len(ocr_models):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    model = ocr_models[model_id - 1]
    if file:
        return model.file_path
    return OcrModelResponse(**model.dict())

def update_ocr_model(
        model_id: str,
        counter_id: str,
        collected_info: list[str],
        model_file: UploadFile | None,
) -> OcrModelResponse:
    if model_id > len(ocr_models):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    model = ocr_models[int(model_id) - 1]
    model.counter_id = counter_id
    model.collected_info = collected_info
    model.updated_at = datetime.now()
    if model_file:
        with open(f'ocr-models/{model_file.filename}', 'wb') as f:
            f.write(model_file.file.read())
        model.file_path = f'ocr-models/{model_file.filename}'
    return OcrModelResponse(**model.dict())

def delete_ocr_model(model_id: str):
    if model_id > len(ocr_models):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    ocr_models.pop(model_id - 1)

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
        
        # TODO: Make upload_image_to_cloudinary a background task
        # uploaded_image_url = upload_image_to_cloudinary(file_path)
        # results = get_digits_from_image(file_path)
        # print(results)
        results = collected_info_values

        model_id = None
        for model in ocr_models:
            if model.counter_id == counter_id:
                model_id = model.id
                break
        # create a data object
        data_obj = DataInDB(
            _id=str(len(data) + 1),
            counter_id=str(counter_id),
            ocr_model_id=str(model_id),
            flavor=flavor,
            size=size,
            file_url=None,
            collected_info_values=results,
            uploader_username=current_user.username,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        data.append(data_obj)
        background_tasks.add_task(upload_image_and_write_data_to_gsheet, file_path, data_obj)
        return DataResponse(**data_obj.dict())

def get_data_ids(counter_id: str | None, flavor: str | None, size: str | None, uploader_username: str | None, start_date: str | None, end_date: str | None) -> list[DataResponse]:
    data_in_db = []
    for data_obj in data:
        if (counter_id is None or data_obj.counter_id == counter_id) and \
                (flavor is None or data_obj.flavor == flavor) and \
                (size is None or data_obj.size == size) and \
                (uploader_username is None or data_obj.uploader_username == uploader_username) and \
                (start_date is None or data_obj.created_at >= datetime.fromisoformat(start_date)) and \
                (end_date is None or data_obj.created_at <= datetime.fromisoformat(end_date)):
            data_in_db.append(DataResponse(**data_obj.dict()))
    return data_in_db

def get_data(data_id: str, file: bool = False) -> DataResponse:
    data_id = int(data_id)
    if data_id > len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    data_obj = data[data_id - 1]
    if file:
        with open(data_obj.file_path, 'rb') as f:
            file_content = f.read()
        return DataResponse(**data_obj.dict(), file=file_content)
    return DataResponse(**data_obj.dict())

def update_data(
        data_id: str,
        counter_id: str,
        flavor: str,
        size: str,
        collected_info_values: object,
        data_file: UploadFile | None,
) -> DataResponse:
    if data_id > len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    data_obj = data[int(data_id) - 1]
    data_obj.counter_id = counter_id
    data_obj.flavor = flavor
    data_obj.size = size
    data_obj.collected_info_values = collected_info_values
    data_obj.updated_at = datetime.now()
    if data_file:
        with open(f'data/{data_file.filename}', 'wb') as f:
            f.write(data_file.file.read())
            file_path = f'data/{data_file.filename}'
        uploaded_image_url = upload_image_to_cloudinary(file_path)
        data_obj.file_url = uploaded_image_url
    return DataResponse(**data_obj.dict())

def delete_data(data_id: str):
    if data_id > len(data):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    data.pop(data_id - 1)


def upload_image_and_write_data_to_gsheet(
        file_path: str,
        data_entry_obj: DataInDB,
):
    uploaded_image_url = upload_image_to_cloudinary(file_path)
    data_entry_obj.file_url = uploaded_image_url
    write_data_entry_to_gsheet(data_entry_obj)



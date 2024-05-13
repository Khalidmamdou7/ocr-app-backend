# router.py
# Defining the API endpoints go here and calling the service layer


from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import Field

from ..models import ResponseModel
from ..auth.dependencies import authenticate_user_jwt, get_current_user
from ..auth.models import RoleEnum, User

from . import service as data_gathering_service
from .models import *


router = APIRouter()

@router.post("/ocr-models", response_model=ResponseModel[OcrModelResponse], status_code=status.HTTP_201_CREATED)
async def upload_ocr_model(
    background_tasks: BackgroundTasks,
    ocr_model_file: UploadFile = File(...),
    collected_info: list[str] = [],
    counter_id: str = None,
    current_user: User = Depends(get_current_user)
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
    collected_info = collected_info[0].split(',') if collected_info[0] else []
    ocr_model = await data_gathering_service.upload_ocr_model(ocr_model_file, counter_id, collected_info, background_tasks)

    return ResponseModel(
        data=ocr_model,
        message="model uploaded successfully",
        status="success",
    )

@router.get("/ocr-models", response_model=ResponseModel[list[OcrModelResponse]])
def get_ocr_models_ids(counter_id: str | None):
    ocr_models = data_gathering_service.get_ocr_models_ids(counter_id)

    return ResponseModel(
        data=ocr_models,
        message="models retrieved successfully",
        status="success",
    )

@router.get("/ocr-models/{ocr_model_id}", response_model=ResponseModel[OcrModelResponse])
async def get_model(ocr_model_id: str):
    ocr_model = await data_gathering_service.get_ocr_model(ocr_model_id, False)

    return ResponseModel(
        data=ocr_model,
        message="model retrieved successfully",
        status="success",
    )

@router.get("/ocr-models/{ocr_model_id}/file", response_class=FileResponse)
async def get_model_file(ocr_model_id: str):
    file_path = await data_gathering_service.get_ocr_model(ocr_model_id, True)

    return FileResponse(file_path)


@router.put("/ocr_models/{ocr_model_id}", response_model=ResponseModel[OcrModelResponse])
async def update_ocr_model(
    ocr_model_id: str,
    counter_id: str,
    collected_info: list[str],
    ocr_model_file: UploadFile | None = None,
    current_user: User = Depends(get_current_user)
):
    if current_user.role == RoleEnum.WORKER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    ocr_model = data_gathering_service.update_ocr_model(ocr_model_id, counter_id, collected_info, ocr_model_file)

    return ResponseModel(
        data=ocr_model,
        message="model updated successfully",
        status="success",
    )


@router.delete("/ocr_models/{ocr_model_id}", response_model=ResponseModel[None])
def delete_ocr_model(ocr_model_id: str):
    data_gathering_service.delete_ocr_model(ocr_model_id)

    return ResponseModel(
        data=None,
        message="model deleted successfully",
        status="success",
    )

@router.post("/data", response_model=ResponseModel[DataResponse], status_code=status.HTTP_201_CREATED)
async def upload_data(
    background_tasks: BackgroundTasks,
    data_file: Annotated[UploadFile, File(...)],
    counter_id: Annotated[str, Form(...)],
    flavor: Annotated[str, Form(...)],
    size: Annotated[str, Form(...)],
    collected_info_values: Annotated[dict | None, Form(...)] = None,
    current_user: User = Depends(get_current_user),
):
    data = await data_gathering_service.upload_data(data_file, counter_id, flavor, size, collected_info_values, current_user, background_tasks)
    print(data)
    return ResponseModel(
        data=data,
        message="data uploaded successfully",
        status="success",
    )


# TODO FIXME: This endpoint is not working
# @router.get("/data", response_model=ResponseModel[list[DataResponse]])
# def get_data_ids(
#     counter_id: int | None,
#     flavor: str | None,
#     size: str | None,
#     user_id: str | None,
#     start_date: str | None,
#     end_date: str | None,
# ):
#     print(counter_id, flavor, size, user_id, start_date, end_date)
#     data = data_gathering_service.get_data_ids(
#         counter_id,
#         flavor, size,
#         user_id,
#         start_date,
#         end_date,
#     )
#     print(data)

#     return ResponseModel(
#         data=data,
#         message="data retrieved successfully",
#         status="success",
#     )

@router.get("/data/{data_id}", response_model=ResponseModel[DataResponse])
def get_data(data_id: str):
    data = data_gathering_service.get_data(data_id)

    return ResponseModel(
        data=data,
        message="data retrieved successfully",
        status="success",
    )
    
@router.put("/data/{data_id}", response_model=ResponseModel[DataResponse])
async def update_data(
    data_id: str,
    data: UploadFile = File(...),
    counter_id: str = None,
    flavor: str = None,
    size: str = None,
    collected_info_values: object = None,
    current_user: User = Depends(get_current_user)
):
    data = data_gathering_service.update_data(data_id, data, counter_id, flavor, size, collected_info_values, current_user)

    return ResponseModel(
        data=data,
        message="data updated successfully",
        status="success",
    )

@router.delete("/data/{data_id}", response_model=ResponseModel[None])
def delete_data(data_id: str):
    data_gathering_service.delete_data(data_id)

    return ResponseModel(
        data=None,
        message="data deleted successfully",
        status="success",
    )


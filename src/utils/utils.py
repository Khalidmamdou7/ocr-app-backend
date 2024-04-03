from typing import Any, Optional

from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)

def id_to_str(dict: dict) -> dict:
    """Converts the id field of a dict to a string."""
    if "_id" in dict:
        dict["id"] = str(dict["_id"])
    dict["_id"] = dict["id"]
    return dict

def db_to_dict(db_obj: Optional[dict]) -> dict:
    """Converts a database object to a dict."""
    if db_obj is not None:
        id_to_str(db_obj)
        return db_obj
    else:
        raise Exception("Object not found")

def obj_to_dict(obj) -> dict:
    """Converts an object to a dict."""
    if obj is not None:
        dict = obj.dict()
        id_to_str(dict)
        dict["_id"] = str(dict["id"])
        return dict
    else:
        raise Exception("Object not found")

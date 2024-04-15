import re
from typing import Optional, List
from bson import ObjectId
from dataclasses import dataclass, asdict
from pydantic import BaseModel, Field, validator
from pydantic import BaseModel, validator, root_validator
from datetime import datetime
from datetime import timedelta
import secrets


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SensorTimeSeries(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    equipment_id: str = Field("")
    value: float = Field(0)
    timestamp: datetime = Field(default_factory=datetime.utcnow().isoformat())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "equipment_id": "sensor1",
                "value": 1.0,
                "timestamp": "2021-09-01T12:00:00-05:00",
            }
        }


class Sensor(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    equipment_id: str = Field("")
    name: str = Field(f"sensor-{equipment_id}")
    type: str = Field("sensor")
    created_at: datetime = Field(default_factory=datetime.utcnow().isoformat())
    updated_at: datetime = Field(default_factory=datetime.utcnow().isoformat())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "equipment_id": "sensor1",
                "name": "sensor-1",
                "type": "sensor",
                "created_at": "2021-09-01T12:00:00-05:00",
                "updated_at": "2021-09-01T12:00:00-05:00",
            }
        }

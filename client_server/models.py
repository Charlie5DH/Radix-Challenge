import datetime
from pydantic import BaseModel
from enum import Enum


class Sensor(BaseModel):
    equipmentId: str
    name: str
    type: str = "sensor"
    createdAt: datetime.datetime = datetime.datetime.now()
    updatedAt: datetime.datetime = datetime.datetime.now()


class Notification(BaseModel):
    equipmentId: str
    type: str = "notification"
    message: str = f"Notification from {datetime.datetime.now()}"
    createdAt: datetime.datetime = datetime.datetime.now()
    updatedAt: datetime.datetime = datetime.datetime.now()


class FormatOptions(Enum):
    dict = 'dict'
    list = 'list'
    series = 'series'
    split = 'split'
    tight = 'tight'
    records = 'records'
    index = 'index'


class JoinOptions(Enum):
    inner = 'inner'
    left = 'left'
    right = 'right'
    outer = 'outer'
    cross = 'cross'

from pydantic import BaseModel
from datetime import datetime

class Record(BaseModel):
    device_name: str
    time: datetime
    temp: int
    humi: int
    led1: bool
    led2: bool

class Temp(BaseModel):
    device_name: str
    time: datetime
    temp: int

class Humi(BaseModel):
    device_name: str
    time: datetime
    humi: int

class Led1(BaseModel):
    device_name: str
    time: datetime
    led1: bool

class Led2(BaseModel):
    device_name: str
    time: datetime
    led2: bool

from pydantic import BaseModel
from datetime import datetime
from typing import Any


class Record(BaseModel):
    device_name: str
    data: dict
    
class Temp(BaseModel):
    device_name: str
    temp: int

class Humi(BaseModel):
    device_name: str
    humi: int

class Led1(BaseModel):
    device_name: str
    led1: bool

class Led2(BaseModel):
    device_name: str
    led2: bool

class Ultra(BaseModel):
    device_name: str
    ultra: int

class Rotary(BaseModel):
    device_name: str
    rotary: int
from pydantic import BaseModel
from datetime import datetime

class Record(BaseModel):
    device_name: str
    time: datetime
    tem: int
    humi: int
    led1: bool
    led2: bool
from pydantic import BaseModel
from datetime import datetime

class Temp(BaseModel):
    device_name: str
    time: datetime
    temp: int

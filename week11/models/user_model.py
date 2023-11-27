from pydantic import BaseModel

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

class Ledstick(BaseModel):
    device_name: str
    ledstick: int

class Digit(BaseModel):
    device_name: str
    digit: int

class Sonic(BaseModel):
    device_name: str
    sonic: int

class Light(BaseModel):
    device_name: str
    light: int

class Lcd(BaseModel):
    device_name: str
    lcd: str

class Thump(BaseModel):
    device_name: str
    thump: int
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn
import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

appp = FastAPI()

class Item(BaseModel):
    data1: int
    data2: int

@appp.get("/")
async def root():
    return {"message": "Hello"}

@appp.get("/update")
async def update_data(data1: int, data2: int):
    return {"data1": data1, "data2": data2}  

@appp.post("/update_post")
async def update_data_post(item: Item):
    mydict = {"data1": item.data1, "data2": item.data2}
    print(mydict)
    return("OK")

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
# 	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
# 	logging.error(f"{request}: {exc_str}")
# 	content = {'status_code': 10422, 'message': exc_str, 'data': None}
# 	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

if __name__=="__main__":
    uvicorn.run("server:appp", port=8000, reload=True, access_log=True)
from fastapi import FastAPI
from routes.record_router import record


app = FastAPI()

app.include_router(record)

@app.get("/")
async def home():
    return {"message": "Hello World"}


from fastapi import FastAPI
from routes.record_router import record
import uvicorn

app = FastAPI()

app.include_router(record)

@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True, access_log=True, host="192.168.1.17")
from typing import Dict, Any

from fastapi import FastAPI

app = FastAPI()

@app.post("/example")
async def post_example(data: Dict[str, Any]):
    print(type(data))
    return data

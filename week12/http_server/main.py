from fastapi import FastAPI

app = FastAPI()

@app.get("/example")
async def get_example(**kwargs):
    return kwargs

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import Record, Temp, Humi, Led1, Led2, Ledstick, Digit, Sonic , Light, Lcd, Thump, Graph
import uvicorn

app = FastAPI()

host = "192.168.1.14"
class NotAuthenticatedException(Exception):
    pass

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request, exc):
    return RedirectResponse(url='/login')

app.include_router(Record.record, tags= ["Record"])

app.include_router(Temp.temp, tags= ["Temp"])

app.include_router(Humi.humi, tags= ["Humi"])

app.include_router(Led1.led1, tags= ["Led1"])

app.include_router(Led2.led2, tags= ["Led2"])

app.include_router(Ledstick.ledstick, tags= ["LEDSTICK"])

app.include_router(Digit.digit, tags= ["DIGIT"])

app.include_router(Sonic.sonic, tags= ["Sonic"])

app.include_router(Light.light, tags= ["Light"])

app.include_router(Lcd.lcd, tags= ["LCD"])

app.include_router(Thump.thump, tags= ["Thump"])

app.include_router(Graph.graph, tags=["Graph"])

@app.get("/")
async def home():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True, access_log=True)
from fastapi import APIRouter, HTTPException
from  config.db import *
from schemas.schema import *
from schemas import *
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
from fastapi import FastAPI, Depends, Request, Response, status
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from io import BytesIO
import base64


graph = APIRouter()

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True)
manager.cookie_name = "some-name"
DB = {
    'users': {
        'test@mail.com': {
            'name': 'TEST USER',
            'password': 'test'
        }
    }
}

def query_user(user_id: str):
    return DB['users'].get(user_id)

@manager.user_loader()
def load_user(user_id: str):
    user = DB['users'].get(user_id)
    return user
 

@graph.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Đăng Nhập</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            form {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 300px;
                text-align: center;
            }

            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
            }

            input {
                width: 100%;
                padding: 8px;
                margin-bottom: 15px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            input[type="submit"] {
                background-color: #4caf50;
                color: #fff;
                cursor: pointer;
            }

            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <form method="POST" action="/login">
            <h1>Đăng Nhập</h1>
            <label for="username">Email:</label>
            <input type="text" id="username" name="username" value="" required>
            <label for="password">Mật Khẩu:</label>
            <input type="password" id="password" name="password" value="" required>
            <input type="submit" value="Đăng Nhập">
        </form>
    </body>
    </html>
    """

@graph.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = query_user(email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    token = manager.create_access_token(data={'sub': email})
    response = RedirectResponse(url="/graph",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(response, token)
    return response

def get_value_time(datas: list, field: str):
    time = []
    value = []
    for x in datas:
        value.append(x[field])
        t = x["time"]
        time.append(x["time"])
    return value, time

def draw_graph():
    temp =  temps_serializer(collection_temp.find({}).sort([['_id', -1]] ))
    temp_value, time_temp = get_value_time(temp, "temp")

    humi =  humis_serializer(collection_humi.find({}).sort([['_id', -1]] ))
    humi_value, time_humi = get_value_time(humi, "humi")

    led1 =  led1s_serializer(collection_led1.find({}).sort([['_id', -1]] ))
    led1_value, time_led1 = get_value_time(led1, "led1")

    led2 =  led2s_serializer(collection_led2.find({}).sort([['_id', -1]] ))
    led2_value, time_led2 = get_value_time(led2, "led2")

    ledstick =  ledsticks_serializer(collection_ledstick.find({}).sort([['_id', -1]] ))
    ledstick_value, time_ledstick = get_value_time(ledstick, "ledstick")

    sonic =  sonics_serializer(collection_sonic.find({}).sort([['_id', -1]] ))
    sonic_value, time_sonic = get_value_time(sonic, "sonic")

    light =  lights_serializer(collection_light.find({}).sort([['_id', -1]] ))
    light_value, time_light = get_value_time(light, "light")

    thump =  thumps_serializer(collection_thump.find({}).sort([['_id', -1]] ))
    thump_value, time_thump = get_value_time(thump, "thump")

    plt.figure(figsize=(10, 8))

    plt.subplot(4, 2, 1)
    plt.plot(time_temp, temp_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('TEMP')
    plt.title('TEMP GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45) 
    

    plt.subplot(4, 2, 2)
    plt.plot(time_humi, humi_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('HUMI')
    plt.title('HUMI GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 3)
    plt.plot(time_led1, led1_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('LED1')
    plt.title('LED1 GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 4)
    plt.plot(time_led2, led2_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('LED2')
    plt.title('LED2 GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 5)
    plt.plot(time_sonic, sonic_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('sonic')
    plt.title('sonic GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 6)
    plt.plot(time_light, light_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('light')
    plt.title('light GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 7)
    plt.plot(time_ledstick, ledstick_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('ledstick')
    plt.title('ledstick GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    plt.subplot(4, 2, 8)
    plt.plot(time_thump, thump_value, marker='o', linestyle='-')
    plt.xlabel('time')
    plt.ylabel('thump')
    plt.title('thump GRAPH')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S\n%y,%m,%d'))
    plt.xticks(rotation=45)

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png',  bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    return img_base64

@graph.get('/tgraph',  response_class=HTMLResponse)
def drw_graph():
    draw_graph()

@graph.get('/graph',  response_class=HTMLResponse)
def protected_route(user=Depends(manager)):
    img_base64 = draw_graph()
    html_content = """
    <html>
        <head>
            <title>Graph</title>
        </head>
        <body>
            <h1>ĐỒ THỊ CÁC GIÁ TRỊ CẢM BIẾN</h1>
            <img src="data:image/png;base64,{}" />
        </body>
    </html>
    """.format(img_base64)
    return HTMLResponse(content=html_content)
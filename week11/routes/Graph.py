from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from auth import auth
import matplotlib.pyplot as plt
from  config.db import *
from io import BytesIO
import base64
from schemas.schema import *
import pandas as pd
import io
import base64
from datetime import datetime
import json

graph = APIRouter()


def plot_graph(data, title, xlabel, ylabel, color='b'):
    # Chuyển đổi dữ liệu từ chuỗi JSON thành đối tượng Python
    data_list = json.loads(data)

    # Trích xuất thông tin từ danh sách dữ liệu
    times = [datetime.strptime(entry["time"], "%Y-%m-%dT%H:%M:%S.%f") for entry in data_list]
    values = [entry.get("temp", entry.get("humi")) for entry in data_list]

    # Tạo đồ thị
    plt.plot(times, values, marker='o', linestyle='-', label=title, color=color)


def list_data(data):
    result = []
    time = []
    for item in data:
        result.append(item['temp'])
        time.append(item["time"]) 
    return result. time


def get_all():
    temp = temps_serializer(collection_temp.find({}).sort([['_id', -1]] ))
    humi = humis_serializer(collection_humi.find({}).sort([['_id', -1]] ))
    led1 = led1s_serializer(collection_led1.find({}).sort([['_id', -1]] ))
    led2 = led2s_serializer(collection_led2.find({}).sort([['_id', -1]] ))

    temp_list, temp_time = list_data(temp)
    plt.figure()

    plt.subplot(2, 2, 1)
    plt.plot(temp_time,temp_list)
    plt.xlabel('Time')
    plt.ylabel('Temp')
    plt.legend()

    plt.suptitle('GRAPH')

    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')
    return img_base64

    

@graph.get("/graph", response_class=HTMLResponse)
def display_graph():
    
    img_base64 = get_all()

    html_content = f"""
    <html>
    <head>
        <title>GRAPH</title>
        <meta http-equiv="refresh" content="5" >
    </head>
    <body>
        <h1>SHOW DATA</h1>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    """
    return html_content
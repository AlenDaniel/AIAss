# 客户端拉取数据与展示

from typing import Union
from fastapi import FastAPI,BackgroundTasks

# 跨目录访问
import sys
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loguru import logger as logg

#自定义模块
from app.app_config import *
from src.parser import *


# 初始化

app = FastAPI()
dt = Datatool()


# 主页index
@app.get('/')
def index():
    return{'hello:world'}


# 从设备端获取数据至客户端示波器
@app.post('/send/data/')
def getData(data:appData,bkt:BackgroundTasks):
    if data is None:
        return '上传数据不对'
    bkt.add_task(dt.parseData,data)
    logg.info('接收到新的数据')
    return '数据已经获取，正在处理中'
    












# 测试接口
# @app.get('/')
# def read_root():
#     return {'hello:world'}

# # 测试接口2
# @app.get('/items/{item_id}')
# def back(item_id:int,q:Union[str,None]=None):
#     return {'item_id':item_id,"q":q}

# # 测试接口3
# @app.put('/items/{item_id}')
# def update_item(item_id:int,item:Item):
#     return {'item_name':item.name,'item_id':item_id}

# # 测试接口
# @app.post('/app/data/send/')
# def update_data(item:appData):
#     return item
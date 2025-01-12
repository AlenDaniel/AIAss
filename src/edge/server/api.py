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
from edg_congfig import *


# 初始化

app = FastAPI()


# 
@app.get('/get/data')
def index():
    return 200



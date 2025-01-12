# 这是一个数据配置模块

from pydantic import BaseModel
from typing import Union

# 日志数据
iconPath = 'http://0.0.0.0:5500/get/data'
logName = "./log/AICall_app.log"
logSubject = "AICall_app 日志告警"



# 服务器参数
httpServer = dict(uname ='0.0.0.0',
    paths = "api:app",
    ports = 8088,
    log = 'info',
    reloade =True)

#本地数据保存
fileName  = './Data/data.xlsx'


# {
#     'uname':'127.0.0.1',
#     "paths":"api:app",
#     "ports":8088,
#     "log":'info',
#     "reloade":True
# }

# 绘制线条参数
Delta = {
    "name":"Delta",
    "width":1, 
    "bcolor":"#e05612",
    "roll":[0,0],  #分图
    
}
Theta = {
    "name":"Theta",
    "width":1, 
    "bcolor":"#f49d1a",
    "roll":[0,1],  #分图
    
}
LowAlpha = {
    "name":"LowAlpha",
    "width":1, 
    "bcolor":"#b83af6",
    "roll":[1,0],  #分图
    
}
HighAlpha = {
    "name":"HighAlpha",
    "width":1, 
    "bcolor":"#ec5b69",
    "roll":[1,1],  #分图
    
}
LowBeta = {
    "name":"LowBeta",
    "width":1, 
    "bcolor":"#2aabd6",
    "roll":[2,0],  #分图
    
}
HighBeta = {
    "name":"HighBeta",
    "width":1, 
    "bcolor":"#aced27",
    "roll":[2,1],  #分图
    
}
LowGamma = {
    "name":"LowGamma",
    "width":1, 
    "bcolor":"#4cf1f1",
    "roll":[3,0],  #分图
    
}
MiddleGamma = {
    "name":"MiddleGamma",
    "width":1, 
    "bcolor":"#dd9ec2",
    "roll":[3,1],  #分图
    
}
Attentio = {
    "name":"Attentio",
    "width":1, 
    "bcolor":"#b5bdba",
    "roll":[4,0],  #分图
    
}
Meditation = {
    "name":"Attentio",
    "width":1, 
    "bcolor":"#248c0d",
    "roll":[4,1],  #分图
    
}


# 测试数据
class Item(BaseModel):
    name:str
    price:float
    is_offer: Union[bool,None] = None

# 终端上传数据
class appData(BaseModel):
    data:list

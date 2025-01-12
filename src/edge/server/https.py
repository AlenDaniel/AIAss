# 网络访问模块

# 跨目录访问
import sys
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from loguru import logger as logg

# 自定义模块
from edg_congfig import *

import uvicorn
from fastapi import BackgroundTasks

class Server():
    def __init__(self,paths=str,uname=str,ports=int,log=str,reloade=bool) -> None:
        config = uvicorn.Config(paths, host=uname, port=ports, log_level=log,reload=reloade)
        server = uvicorn.Server(config)
        self.server = server
    
    def run(self):
        self.server.run()


@logg.catch
# 启动服务
def serverRun():
    sh = Server(**httpServer)
    logg.info('服务器初始化已完成，正在启动……')
    BackgroundTasks.add_task(sh.run)
    logg.info('服务已开启！')


    # 这是一个用于启动本地服务的模块
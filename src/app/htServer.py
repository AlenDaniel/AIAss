# 这是一个用于启动本地服务的模块

import os

import uvicorn

class Server():
    def __init__(self,paths=str,uname=str,ports=int,log=str,reloade=bool) -> None:
        config = uvicorn.Config(paths, host=uname, port=ports, log_level=log,reload=reloade)
        server = uvicorn.Server(config)
        self.server = server
    
    def run(self):
        self.server.run()

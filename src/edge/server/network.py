# 这是一个用于http数据链接的库
import requests as rq
import json
from loguru import logger as log

# 自定义模块
from edg_congfig import *

class HTTP():
    def __init__(self) -> None:
        self.url = ttlPath
        pass

    # 获取服务数据
    @log.catch
    def get(self,url=None):
        if url is None:
            url = self.url
        backData = rq.get(url)
        return backData
    
    # post发送服务数据
    @log.catch
    def post(self,data,url=None):
        if data is None:
            return

        if url is None:
            url = self.url
        jsondata = json.dumps({'data':data})
        backData = rq.post(url,data=jsondata)
        if backData and backData.status_code == 200:
            log.info('数据已发送')
        return backData
    
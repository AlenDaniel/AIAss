import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# project_root = os.path.dirname(os.path.abspath(__file__)) 
# sys.path.insert(0, project_root)

# 系统模块

# 自定义模块
from plugin import loger
from edg_congfig import *
from src.ttl import BCIDATA
from server.https import *




# 主入口执行
if __name__ == '__main__':
    # 日志准备
    logger = loger.Log(logName,logSubject)
    log = logger.get()
    bci = BCIDATA('/dev/ttyUSB0')
    log.info('初始化完成')
    serverRun()
    log.info('远程服务已启动')
    bci.start()
    log.info('硬件信道已建成,数据采集正在作业……')
    bci.render()
    
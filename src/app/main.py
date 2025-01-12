# 跨目录访问
import sys
import os
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# 自定义模块

from plugin.loger import *
from app.app_config import *

from htServer import *

from AICall.incall import *

if __name__ == "__main__":
    logger = Log(logName,logSubject)
    logg = logger.get()
    # sh = Server(**httpServer)
    pid = os.getpid()
    log.info('服务器初始化已完成，正在启动……')
    log.info(f'服务器进程号{pid}')
    print(pid)
    # sh.run()
    print('服务已运行！')
    init()
    log.info('服务已开启！')
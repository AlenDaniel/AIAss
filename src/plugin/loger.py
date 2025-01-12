# 这是一个日志库 附带告警

import sys
import notifiers
from loguru import logger as log
from notifiers.logging import NotificationHandler

# 自定义模块
from .plugin_config import *


class Log():
    def __init__(self,name = str,subject=str) -> None:
        
        # 参数初始化
        if name is None:
            name = './log/default.log'
        if subject is  not None:
            Notify['subject'] = subject
        
        # 日志告警
        notifier = notifiers.get_notifier("email")
        notifier.notify(message="来电日志", **Notify)

        # 发生Error时，邮件告警
        handler = NotificationHandler("email", defaults=Notify)

        #初始化日志文件
        log.remove(0)

        # 添加日志文件
        log.add(name,rotation='00:00',level='INFO',encoding="utf-8", enqueue=True,)
        log.add(handler,level='WARNING')
        
        #变量输出
        self.log = log
        pass
    
    # 获取log变量
    def get(self):
        if self.log:
            return self.log
        pass



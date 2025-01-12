# 这是一个日志库 附带告警

import sys
import notifiers
from loguru import logger as log
from notifiers.logging import NotificationHandler
from notifiers import get_notifier

# 自定义模块
from .plugin_config import *


class Log():
    def __init__(self,name = str,subject=str) -> None:
        
        # 参数初始化
        if name is None:
            name = './log/default.log'
        if subject is  not None:
            Notify['subject'] = subject
        
        
        # 日志初始化
        notifier = notifiers.get_notifier("email")
        notifier.notify(message="终端日志记录", **Notify)

        # 发生业务时，邮件通知
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



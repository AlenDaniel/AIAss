import sys
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

# import os
# sys.path.append(os.path.join(os.getcwd(), '..'))

# 系统模块
import serial
import time

from loguru import logger as log

# 自定义模块
from .parser_data import Parser

class BCIDATA():
    def __init__(self,port='/dev/ttyUSB0'):
        self.port = port
        self.baurate = 9600
        self.concentration = 0
        self.ser = None
        self.Pa = Parser()

    # 初始化硬件
    @log.catch
    def start(self):
        self.ser = serial.Serial(
            port = self.port,
            baudrate = self.baurate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
                )
    
    # 读取数据
    @log.catch
    def render(self):
        ser = self.ser
        while not ser.isOpen():
            log.info(f'正在建立连接……')
            time.sleep(5)
        while True:
            n =  ser.inWaiting()
            data = ser.read(n)
            if len(data)>0:
                log.info('以获取到数据')
                self.Pa.decompose(data)
            time.sleep(0.7)
    
    #测试读取单元
    @log.catch
    def testrender(self):
        while not self.ser.isOpen():
            log.info(f'请等待……测试设备正在连接中……')
            time.sleep(3)

        while self.ser.inWaiting() > 0:
            n = self.ser.inWaiting()
            log.info('正在读取数据')
            self.ser.read(self.ser.inWaiting())
            time.sleep(0.1)

        while True:
            data = self.ser.read_all()
            if not data:
                time.sleep(0.01)
                continue
            if data:
                self.cocentration = data


    # while True:
    #     n = bci.ser.inWaiting()
    #     if n:
    #         data = bci.ser.read(n)
    #         value = [int(hex(num),16)for num in data]
    #         print(len(value[6:]))
    #         print(f'val:{value[6:]}')
    #     time.sleep(2)


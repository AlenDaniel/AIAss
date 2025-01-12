# 这是一个用于解析BCI数据的库
import sys
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from loguru import logger as log


# 自定义模块
from tool.show import Graphic
from server.network import HTTP


class Parser():
    def __init__(self):
        self.start = 7
        self.Signal = [int(x,16) for x in ['0x1D','0x36','0x37','0x38','0x50','0x51','0x52','0x6B','0xC8']]  #5,6位 信号表达式
        self.SignalA = 7
        self.SignalLen = 24 #7位信号长度
        self.Delta = []
        self.Theta = []
        self.LowAlpha = []
        self.HighAlpha = []
        self.LowBeta = []
        self.HighBeta = []
        self.LowGamma = []
        self.MiddleGamma = []
        self.Attentio = 0
        self.Meditation = 0
        self.tail = 0
        self.Grp = Graphic()
        self.htp = HTTP()

    # 分解数据
    # @log.catch
    def decompose(self,bytedata):
        if bytedata is None:
            return
        if len(bytedata)>0:
            valuedata = [hex(num) for num in bytedata]
            lenData = len(valuedata)
            if lenData>0:
                if lenData>=36:
                    for x in range(int(lenData/36)):
                        pareData = valuedata[int(36*x):int(36*(x+1))]

                        # 检测数据是否正常
                        ckeck = self.checkDevice(pareData[3:5])

                        # 检索数据
                        data = self.getData(pareData)

                        #回传数据至服务器
                        self.sendData(data)

                        # 本地可视化数据
                        # self.scope(data)
                        

                        return data
    
    # 读取设备数据
    @log.catch
    def getData(self,data):
        if data is None:
            return
        sum = int(data[6],16)
        if sum == self.SignalLen:
            dtlist = ['','','','','','','','']
            # dtlist = [self.Delta,self.Theta,self.LowAlpha,self.HighAlpha,self.LowBeta,self.HighBeta,self.LowGamma,self.MiddleGamma]
            for index, x in enumerate( data[7:31]):
                ix = int(index/3)
                value = int(x,16)
                dtlist[ix] = dtlist[ix] + str(value)
            self.Attentio=int(data[32],16)
            self.Meditation=int(data[34],16)
            dtlist.append(self.Attentio)
            dtlist.append(self.Meditation)
            return dtlist
                
    # 示波器（展示设备信息）
    def scope(self,value):
        if value is None:
            return
        if len(value)>0:
            self.Grp.scope(value)
        pass

    # 发送数据至服务器
    @log.catch
    def sendData(self,data):
        if data is None:
            return 
        satus = self.htp.post(data)
        if satus:
            if satus.status_code == 200:
                log.info('数据发送成功')
            else:
                log.warning('数据发送失败')
        else:
            log.warning('数据发送失败')
        return

    # 检测设备状态
    @log.catch
    def checkDevice(self,value):
        if value is None:
            return False
        signal = [int(x,16)for x in value]
        if signal[0] in self.Signal or signal[1] in self.Signal:
            log.warning('设备未佩戴好')
            return False
        else:
            log.info('正在提取数据')
            return True
            

        
        


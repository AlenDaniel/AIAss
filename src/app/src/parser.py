# 这是一个解析处理的展示库
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import time
from loguru import logger as logg

# 自定义模块
from tool.show import Graphic
from server.network import HTTP
from app_config import *

# 数据处理工具
class Datatool():
    def __init__(self) -> None:

        self.enble = False

        # 实时绘制
        # self.gh = Graphic()
        # self.gh.start()
        # self.gh.animation()
        
        # 网络初始化
        self.hp = HTTP()
        # 实时保存数据
        self.localData = pd.DataFrame()



        pass

    def parseData(self,object):
        if object is None:
            return
        pointlist = []
        for tagData in object.data[:-2]:
            point = self.getPointData(tagData)
            # point = self.groupData(tagData)
            pointlist.append(point)
        
        pointlist.append(object.data[8])
        pointlist.append(object.data[9])
        
        # 示波器实时绘制数据更新
        # self.gh.updateData(pointlist)
        
        # 本地存储数据
        self.localData = self.localData._append([pointlist],ignore_index =True)

        logg.info(''.format(self.localData))
        
        # 硬件回调
        if self.enble == False:
            self.enble = True
            self.content()

        return

    # 心跳链接
    def content(self):
        if self.enble:
            while True:
                time.sleep(50)
                backcall = self.hp.get()
                if backcall is None:
                    logg.info('硬件设备连接失败，正在保存为本地数据')
                    self.saveFile()
                    self.enble = False
                    break

    # 数据本地文件保存
    def saveFile(self):
        return
        writer = pd.ExcelWriter(fileName)
        self.localData.to_excel(writer)
        writer.save()

    #按数据类型拆解分组
    def getPointData(self,data):
        if data is None:
            return
        point = int(data,16)
        return point
    
    #按数据类型拆解分组
    def groupData(self,data):
        if data is None:
            return
        
        dlen = len(data)
        point = []
        
        for x in range(int(dlen/3)):
            count = data[x]+data[x+1]+data[x+2]
            point.append(count)
        
        return point


    
    #测试函数 
    def test(self,data=int):
        time.sleep(5)
        logg.info('这是个睡眠测试{}'.format(data))
        print('睡眠测试')





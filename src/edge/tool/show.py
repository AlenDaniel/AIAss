# 这是一个用展示数据的工具类
from matplotlib import pyplot as plt
import numpy as np



class Graphic():
    # 初始化参数
    def __init__(self):
        self.plt=plt
        self.count = 0
        pass
    
    # 示波器
    def scope(self, data):
        if data is None:
            return
        for xd in data[:-2]:
            self.show(xd)
        pass

    # 图标展示
    def show(self, data):
        if data is None:
            return
        for val in data:
            self.plt.plot(self.count,val)
            self.count+=1
        self.plt.show()
        pass
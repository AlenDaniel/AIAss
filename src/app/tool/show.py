# 这是一个用展示数据的工具类
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import time

# 自定义模块
from app_config import *

class Graphic():
    # 初始化参数
    def __init__(self):
        self.plt=plt
        pass

    def start(self):
        self.plt.ion()
        self.fig,self.axs= self.plt.subplots(5,2,sharex=True)  # 创建画布和绘图区
        plt.suptitle("Oscilloscope Display")
        self.enale = True
        self.count = 0
        self.xcount = [0]
        self.Delta = self.line(**Delta)
        self.Theta = self.line(**Theta)
        self.LowAlpha = self.line(**LowAlpha)
        self.HighAlpha = self.line(**HighAlpha)
        self.LowBeta = self.line(**LowBeta)
        self.HighBeta = self.line(**HighBeta)
        self.LowGamma = self.line(**LowGamma)
        self.MiddleGamma = self.line(**MiddleGamma)
        self.Attentio = self.line(**Attentio)
        self.Meditation = self.line(**Meditation)
        self.lineScop = [self.Delta,self.Theta,self.LowAlpha,self.HighAlpha,self.LowBeta,self.HighBeta,self.LowGamma,self.MiddleGamma,self.Attentio,self.Meditation]
        pass

    # 初始化线条
    def line(self,roll = None,name = None,width=None, bcolor = None,style=None):
        y_val = random.randint(20, 100)
        lineA, = self.axs[roll[0],roll[1]].plot(self.xcount, [y_val], color = bcolor, linestyle=style, linewidth = width,label = name)  # 获取折线图对象，逗号不可少，如果没有逗号，得到的是元组
        backLine= {
            'line':lineA,
            'data':[y_val]
        }
        return backLine


    
    # 示波器
    def scope(self, data):
        if data is None:
            return
        self.ax.clear()
        for idx,xd in enumerate(data[:-2]):
            line = self.lineScop[idx]
            self.show(line,xd,idx)
            line.count +=0.01
            # self.show(line,xd)
    
    def updateData(self,data):
        if data is None:
            return
        if self.enale == False:
            self.enale = True
        self.count = self.count + 0.01
        for idx,xd in enumerate(data):
            self.lineScop[idx]['data'].append(xd)
        
        self.xcount.append(self.count)
        pass

    # 图标展示
    def show(self,x):
        data = self.lineScop
        if data is None:
            return
        backlist = []
        for val in data:
            self.plt.cla()
            # val['line'].set_ydata(val['data'])
            val['line'].plot(self.xcount,val['data'])
            # val['line'].set_xdata(self.xcount)
            # self.fig.canvas.draw()
            # self.plt.pause(0.05)
            # backlist.append(val['line'])
        # xline = tuple(backlist)
        # return xline
# 动画循环
    def animate(self,times = 50):
        if self.enale:
            self.animate = FuncAnimation(self.fig, self.show,
                                interval=times,
                                blit=False,  # blitting can't be used with Figure artists
                                repeat_delay=100)
            self.plt.show()
        else:
            return
        pass

    # 直接时间循环
    def animation(self,times=50):
        if self.enale:
            self.plt.show()
            while True:
                time.sleep(50)
                self.plt.draw()
            # self.animate = FuncAnimation(self.fig, self.show,
            #                     interval=times,
            #                     blit=False,  # blitting can't be used with Figure artists
            #                     frames=20,
            #                     repeat_delay=100)
            self.plt.show()
        else:
            return
        pass


# class Line():
#     def __init__(self,name = None,width=None, bcolor = None,style=None):
#         self.plt = plt
#         self.plt.ion()
#         fig, ax = self.plt.subplots()  # 创建画布和绘图区
#         self.Xcount = 0
#         self.line, = ax.plot([0], [50], color = bcolor, linestyle=style, linewidth = width, label = name)  # 获取折线图对象，逗号不可少，如果没有逗号，得到的是元组
    
#     def cleranX(self):
#         if self.Xcount >0:
#             self.Xcount = 0
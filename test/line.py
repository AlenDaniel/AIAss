import time
import matplotlib.pyplot as plt
import numpy as np

# 初始化 figure 和 axes
fig, ax = plt.subplots()

# 初始化 x 轴为时间数据
x = [time.time()]

# 生成不同的y数据集
y1, y2, y3, y4, y5, y6 = [], [], [], [], [], [] 

# 开启交互模式
plt.ion()

while True:

    # 清空旧的绘图
    ax.clear()

    # 计算不同的数据集
    y1.append(np.sin(x[-1]))
    y2.append(np.cos(x[-1]))
    y3.append(x[-1]**2)
    y4.append(x[-1]**3)
    y5.append(np.exp(x[-1])) 
    y6.append(np.log(x[-1]))

    # 绘制每条曲线
    ax.plot(x, y1, label='sin')
    ax.plot(x, y2, label='cos') 
    ax.plot(x, y3, label='x^2')
    ax.plot(x, y4, label='x^3')
    ax.plot(x, y5, label='exp')
    ax.plot(x, y6, label='log')

    # 更新x轴时间数据
    x.append(time.time())

    # 设置图例并显示
    ax.legend()
    fig.canvas.draw()

    # 暂停 Plots must be rested out side of the while loop:
    plt.pause(0.5)

# 关闭交互模式
plt.ioff()
plt.show()
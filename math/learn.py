# -*- coding: utf-8 -*-
"""
 * Created by PyCharm Community Edition.
 * User: nihuan
 * Date: 18-4-3
 * Time: 下午4:55
 """
__author__ = 'nihuan'

import numpy
import matplotlib.pyplot as plot

# 定义存储数组 x 和目标数组 y
x, y = [], []
for sample in open(r'demo/data.txt', 'r'):
# 调用python中的split方法并将逗号作为参数传入
    _x, _y = sample.split(',')
    x.append(float(_x))
    y.append(float(_y))
# 转为numpy数组进一步处理
x, y = numpy.array(x), numpy.array(y)
# 标准化
x = (x-x.mean()) / x.std()
# # 以散点图的形式画出
# plot.figure()
# plot.scatter(x, y, c='g', s=6)
# plot.show()


# 开始训练
x0 = numpy.linspace(-2, 4, 100)


def get_model(deg):
    min_p = numpy.polyfit(x, y, deg)
# 该函数返回L(p;n)最小的参数p，亦即多项式的各项系数
    yy = lambda input_x = x0: numpy.polyval(min_p, input_x)
# 根据输入的值x(默认为x0)，返回预测的值y，
    return yy


# 根据参数n、输入的x,y返回相对应的损失
def get_cost(deg, input_x, input_y):
    return 0.5 * ((get_model(deg)(input_x) - input_y) ** 2).sum()


# 定义几个不同的n进行测试
text = (1, 2, 4, 7, 10)
for d in text:
    print(get_cost(d, x, y))


# 画出相应的图像
plot.scatter(x, y, c='g', s=20)
for d in text:
    plot.plot(x0, get_model(d)(), label='degree={}'.format(d))

plot.xlim(-2, 4)
plot.ylim(1e5, 8e5)
plot.legend()
plot.show()

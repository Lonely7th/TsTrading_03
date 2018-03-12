#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '绘图 工具'
__author__ = 'JN Zhang'
__mtime__ = '2018/1/8'
"""
import numpy as np


# 绘制柱状图
def draw_bar(plt, index, macd_list, macd_trend_list=list(), title='', color='g'):
    plt.subplot(index)
    lable_x = np.arange(len(macd_list))
    lable_y = [x * 0 for x in range(len(macd_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, macd_list, color=color, width=0.6)
    if macd_trend_list:
        for item in macd_trend_list:
            begin = item.get_start_index()
            end = item.get_end_index()
            if item.get_peak_value() > 0:
                plt.bar(lable_x[begin:end], macd_list[begin:end], color='r', width=0.6)
            else:
                plt.bar(lable_x[begin:end], macd_list[begin:end], color='g', width=0.6)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    ylim_min = min(macd_list) * 1.1
    if min(macd_list) * 1.1 > -0.1:
        ylim_min = -0.1
    plt.ylim(ylim_min, max(macd_list) * 1.1)
    plt.title(title)
    plt.grid(True)


# 绘制折线图
def draw_plt(plt, index, data_list, ktrend_list=list(), title='', point1=-1, point2=-1, color="r"):
    plt.subplot(index)
    lable_x = np.arange(len(data_list))
    # 绘制K线
    plt.plot(lable_x, data_list, color=color, linewidth=1.0, linestyle="-")
    # 绘制预测线
    # plt.plot(np.arange(point2, point1+1), data_list[point2:point1+1], color="#00FF00", linewidth=1.6, linestyle="-")
    # 绘制趋势线
    # for item in ktrend_list:
    #     begin = item.get_start_index()
    #     end = item.get_end_index()+1 #保证数据连贯性
    #     if item.get_trend() == 1:
    #         plt.plot(lable_x[begin:end], data_list[begin:end], color="r", linewidth=1.6, linestyle="-")
    #     elif item.get_trend() == -1:
    #         plt.plot(lable_x[begin:end], data_list[begin:end], color="g", linewidth=1.6, linestyle="-")
    # 绘制回测线
    # if point != -1:
    #     plt.plot(lable_x[point:point+10], data_list[point:point+10], color="b", linewidth=1.6, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(data_list) * 0.9, max(data_list) * 1.1)
    plt.title(title)
    plt.grid(True)



def draw_plt_macd(plt, index, price_list, point_list, title=''):
    plt.subplot(index)
    lable_x = np.arange(len(price_list))
    plt.plot(lable_x, price_list, color="#DCDCDC", linewidth=1.6, linestyle="-")
    for point in point_list:
        point_x = [point, point+1]
        point_y = [price_list[point] for point in point_x]
        plt.plot(point_x, point_y, color="#FF0000", linewidth=1.6, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(price_list) * 0.9, max(price_list) * 1.1)
    plt.title(title)
    plt.grid(True)
    pass


def draw_bar_macd(plt, index, macd_list, diff_list, dea_list, title=''):
    plt.subplot(index)
    lable_x = np.arange(len(macd_list))
    lable_y = [x * 0 for x in range(len(macd_list))]
    # 绘制中轴线
    plt.plot(lable_x, lable_y, color="#404040", linewidth=1.0, linestyle="-")
    plt.plot(lable_x, diff_list, color="#7CFC00", linewidth=1.0, linestyle="-")
    plt.plot(lable_x, dea_list, color="#F08080", linewidth=1.0, linestyle="-")
    plt.bar(lable_x, macd_list, color="#DCDCDC", width=0.75)
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(macd_list) * 1.1, max(macd_list) * 1.1)
    plt.title(title)
    plt.grid(True)


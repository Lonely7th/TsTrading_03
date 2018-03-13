#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '策略回测(轻仓版)'
__author__ = 'JN Zhang'
__mtime__ = '2018/3/13'
"""
from utils import draw_utils
from utils.data_utils import fun_01
import matplotlib.pyplot as plt
import numpy as np


# 初始资金
capital_base = 1000000
# 当前持仓
current_position = list()
# 资金池历史记录(用于绘图)
history_capital = list()
# 持仓历史记录(用于绘图)
history_order = list()
# 股票列表
tk_list = list()
# 第二平仓线
k_rate = 0.03
# 第一平仓线
d_rate = -0.03
# 误差数据
error_data = 76
# 最大持仓
max_capital = 0.2


# 模拟卖出操作
def fun_sell(date):
    global capital_base
    while current_position:
        item_order = current_position.pop()
        open_price = tk_list[item_order[0]].get_open_list()[date]
        close_price = tk_list[item_order[0]].get_price_list()[date]
        highest_price = tk_list[item_order[0]].get_highest_list()[date]
        lowest_price = tk_list[item_order[0]].get_lowest_list()[date]
        highest_rate = (highest_price - open_price) / open_price
        lowest_rate = (lowest_price - open_price) / open_price
        close_rate = (close_price - open_price) / open_price
        balance_price = close_price
        if lowest_rate <= d_rate:
            balance_price = open_price * (1+d_rate)
        if highest_rate >= k_rate:
            if close_rate < k_rate:
                balance_price = open_price * (1+k_rate)
        capital_base += balance_price * item_order[2]
        # 统计历史数据
        order_rate = (balance_price-open_price)/open_price
        history_order.append(order_rate)


# 模拟购买操作
def fun_buy(buy_list, date):
    global capital_base
    # 对资金池进行均分
    p_stage = capital_base * max_capital / len(buy_list)
    for index in buy_list:
        # 获取开盘价(默认以每周一的开盘价开仓)
        open_price = tk_list[index].get_open_list()[date]
        if open_price and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                capital_base -= amount * open_price
                current_position.append([index, open_price, amount])


if __name__ == "__main__":
    # 回测14-17年的数据
    for file_name in ["data_price_w_17", "data_price_w_16", "data_price_w_15", "data_price_w_14"]:
        # 初始化数据
        tk_list = [tk for tk in fun_01(file_name) if len(tk.get_wmacd_list()) > error_data]
        capital_base = 1000000
        current_position = list()
        history_capital = list()
        history_order = list()
        # 清洗数据(按照现有的公式计算，列表前部的数据会有一些误差，我们将这些数据清洗掉)
        for tk in tk_list:
            tk.set_wmacd_list(tk.get_wmacd_list()[-error_data:])
            tk.set_price_list(tk.get_price_list()[-error_data:])
            tk.set_diff_list(tk.get_diff_list()[-error_data:])
            tk.set_tur_list(tk.get_tur_list()[-error_data:])
            tk.set_highest_list(tk.get_highest_list()[-error_data:])
            tk.set_open_list(tk.get_open_list()[-error_data:])
            tk.set_lowest_list(tk.get_lowest_list()[-error_data:])

        # 开始执行主要逻辑(模拟时间推移)
        for date in range(26, error_data):
            buy_list = list()  # 待购买列表
            for index in xrange(len(tk_list)):  # 这里item将作为sell_logic的唯一标识
                item_tk = tk_list[index]
                wmacd_list = item_tk.get_wmacd_list()[:]
                price_list = item_tk.get_price_list()[:]
                diff_list = item_tk.get_diff_list()[:]
                dea_list = item_tk.get_dea_list()[:]
                tur_list = item_tk.get_tur_list()[:]
                open_list = item_tk.get_open_list()[:]
                if wmacd_list[date - 1] > 0 >= wmacd_list[date - 2] and 0.1 >= diff_list[date - 1] > 0 and np.mean(
                        tur_list[date - 5:date - 1]) < tur_list[date - 1]:
                    buy_list.append(index)
            if buy_list:  # 如果待购买列表不为空则开单
                fun_buy(buy_list, date)
            # 到此已经完成了开单操作，本周不做任何操作
            # 周五收盘前处理交易单(默认使用本周的收盘价)
            fun_sell(date)
            history_capital.append(capital_base)
        net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
        print file_name, round(net_rate*100, 2), "%"
        # 开始绘图
        plt.figure(figsize=(6, 4), dpi=80)
        draw_utils.draw_plt(plt, 211, history_capital, color="r")
        draw_utils.draw_bar(plt, 212, history_order)
        plt.show()

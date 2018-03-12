#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '策略回测'
__author__ = 'JN Zhang'
__mtime__ = '2018/3/12'
"""
from utils import draw_utils
from utils.data_utils import fun_01
import matplotlib.pyplot as plt
import numpy as np


# 初始数据
capital_base = 1000000
current_position = list()
history_capital = list()
history_order = list()
tk_list = list()
k_rate = 0.03
d_rate = -0.03


def fun_sell(date):
    global capital_base
    while current_position:
        item_order = current_position.pop()
        open_price = tk_list[item_order[0]].get_open_list()[date]
        close_price = tk_list[item_order[0]].get_price_list()[date]
        highest_price = tk_list[item_order[0]].get_highest_list()[date]
        highest_rate = (highest_price - open_price) / open_price
        close_rate = (close_price - open_price) / open_price
        balance_price = close_price
        if close_rate <= d_rate:
            balance_price = open_price * (1+d_rate)
        elif highest_rate >= k_rate:
            if close_rate < k_rate:
                balance_price = open_price * (1+k_rate)
        capital_base += balance_price * item_order[2]
        # 统计历史数据
        order_rate = (balance_price-open_price)/open_price
        history_order.append(order_rate)


def fun_buy(buy_list, date):
    global capital_base
    # 对资金池进行均分
    p_stage = capital_base / len(buy_list)
    for index in buy_list:
        open_price = tk_list[index].get_open_list()[date]
        if open_price and not np.isnan(open_price):
            amount = int(p_stage / open_price / 100) * 100
            if amount >= 100:
                capital_base -= amount * open_price
                current_position.append([index, open_price, amount])


if __name__ == "__main__":
    # 清洗数据
    tk_list = [tk for tk in fun_01() if len(tk.get_wmacd_list()) > 76]
    for tk in tk_list:
        tk.set_wmacd_list(tk.get_wmacd_list()[-76:])
        tk.set_price_list(tk.get_price_list()[-76:])
        tk.set_diff_list(tk.get_diff_list()[-76:])
        tk.set_tur_list(tk.get_tur_list()[-76:])
        tk.set_highest_list(tk.get_highest_list()[-76:])
        tk.set_open_list(tk.get_open_list()[-76:])
    # 以周为单位执行主要逻辑
    for date in range(26, 76):
        # 开始选择标的
        buy_list = list()
        for index in range(len(tk_list)):  # item将作为sell_logic的唯一标识
            item_tk = tk_list[index]
            wmacd_list = item_tk.get_wmacd_list()[:]
            price_list = item_tk.get_price_list()[:]
            diff_list = item_tk.get_diff_list()[:]
            dea_list = item_tk.get_dea_list()[:]
            tur_list = item_tk.get_tur_list()[:]
            open_list = item_tk.get_open_list()[:]
            if wmacd_list[date-1] > 0 >= wmacd_list[date - 2] and 0.1 >= diff_list[date-1] > 0 and np.mean(tur_list[date - 5:date-1]) < tur_list[date-1]:
                buy_list.append(index)
        # 如果开单列表不为空 开单
        if buy_list:
            fun_buy(buy_list, date)
        # 处理交易单(记录当前资金池状态)
        fun_sell(date)
        history_capital.append(capital_base)
    net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]
    print net_rate
    history_capital_rate = list()
    for i in range(1, len(history_capital)):
        cur_vitro = (history_capital[i] - history_capital[i - 1]) / history_capital[i - 1]
        history_capital_rate.append(cur_vitro)
    plt.figure(figsize=(8, 6), dpi=80)
    draw_utils.draw_plt(plt, 311, history_capital, color="r")
    draw_utils.draw_bar(plt, 312, history_order)
    draw_utils.draw_bar(plt, 313, history_capital_rate)
    plt.show()
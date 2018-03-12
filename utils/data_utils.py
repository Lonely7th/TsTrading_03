#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '数据管理 工具'
__author__ = 'JN Zhang'
__mtime__ = '2018/1/18'
"""
import os

from core.tk_mode_bean import tkWModeBean

base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/data"


# 读取数据
def fun_01():
    file_path = base_path + "/data_price_w_18"
    _file = open(file_path)
    tk_list = list()
    while True:
        line = _file.readline()
        if '' == line:
            break
        if '[]' in line:
            continue
        price_list = list(reversed([float(x) for x in line.split("#")[0].strip()[13:-2].split(",")]))
        tur_list = list(reversed([float(x) for x in line.split("#")[1].strip()[1:-2].split(",")]))
        highest_list = list(reversed([float(x) for x in line.split("#")[2].strip()[1:-2].split(",")]))
        open_list = list(reversed([float(x) for x in line.split("#")[3].strip()[1:-2].split(",")]))
        wmacd_list, diff_list, dea_list = fun_02(price_list[:])
        tk_bean = tkWModeBean(line[:11], price_list, wmacd_list, diff_list, dea_list, tur_list, highest_list, open_list)
        tk_list.append(tk_bean)
    return tk_list


# 计算周macd
def fun_02(price_list):
    ema_12_list = list()
    for index in range(len(price_list)):
        if index == 0:
            ema_12_list.append(price_list[0])
        else:
            ema_12_list.append(round(ema_12_list[index-1]*11/13+price_list[index]*2/13, 4))
    ema_26_list = list()
    for index in range(len(price_list)):
        if index == 0:
            ema_26_list.append(price_list[0])
        else:
            ema_26_list.append(round(ema_26_list[index-1] * 25 / 27 + price_list[index] * 2 / 27, 4))
    diff_list = list()
    for index in range(len(ema_12_list)):
        diff = ema_12_list[index] - ema_26_list[index]
        diff_list.append(diff)
    dea_list = list()
    for index in range(len(diff_list)):
        if index == 0:
            dea_list.append(diff_list[0])
        else:
            dea_list.append(round(dea_list[index-1] * 0.8 + diff_list[index] * 0.2, 4))
    wmacd_list = list()
    for index in range(len(dea_list)):
        bar = (diff_list[index] - dea_list[index])*3
        wmacd_list.append(bar)
    return wmacd_list, diff_list, dea_list

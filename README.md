这篇文章主要介绍如何用Python对一些简单的交易策略进行回测。

**1.实现交易策略**

**2.模拟买入和卖出操作**

**3.统计数据和绘图**

源码下载地址：[https://github.com/Lonely7th/TsTrading_03](https://github.com/Lonely7th/TsTrading_03)

**回测结果展示：**
![2014.png](https://upload-images.jianshu.io/upload_images/9225319-05a4b38bbeed73a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![2015.png](https://upload-images.jianshu.io/upload_images/9225319-0503425130d524f9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![2016.png](https://upload-images.jianshu.io/upload_images/9225319-3b33b0238228731b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![2017.png](https://upload-images.jianshu.io/upload_images/9225319-402697b3eb4282a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个交易策略（以下统称策略）是Ts交易模型中的一个，也是相对比较简单且容易实现的一个。
本次回测中我们限制了最大仓位（低于20%），你也可以修改这项限制，对于这个策略而言，增加最大仓位会使得收益率大幅提升。
文章中会着重描述如何使用Python对策略进行回测，不会过多讨论策略的细节和优劣程度，如果你对交易模型或者量化交易感兴趣，可以与我进行交流：1003882179@qq.com

#1.实现交易策略
初始化变量：
```
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
# 误差数据量
error_data = 76
```
加载数据：
```
base_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/data"
file_path = base_path + "/" + file_name
    _file = open(file_path)
    while True:
        line = _file.readline()
        if '' == line:
            break
        if '[]' in line:
            continue
        ...
        tk_bean = tkWModeBean(line[:11], price_list, wmacd_list, diff_list, dea_list, tur_list, highest_list, open_list, lowest_list)
        tk_list.append(tk_bean)
    return tk_list
```
![数据样式](https://upload-images.jianshu.io/upload_images/9225319-52dedf450d13b625.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

清洗数据，执行策略前我们先对数据进行检查和清洗：
```
tk.set_wmacd_list(tk.get_wmacd_list()[-error_data:])
tk.set_price_list(tk.get_price_list()[-error_data:])
tk.set_diff_list(tk.get_diff_list()[-error_data:])
tk.set_tur_list(tk.get_tur_list()[-error_data:])
tk.set_highest_list(tk.get_highest_list()[-error_data:])
tk.set_open_list(tk.get_open_list()[-error_data:])
tk.set_lowest_list(tk.get_lowest_list()[-error_data:])
```
选择标的：
```
if wmacd_list[date - 1] > 0 >= wmacd_list[date - 2] and 0.1 >= diff_list[date - 1] > 0 and np.mean(
    tur_list[date - 5:date - 1]) < tur_list[date - 1]:
        buy_list.append(index)
```
#2.模拟买入和卖出操作
买入操作：
```
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
```
卖出操作：
```
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
```
#3.统计数据和绘图
模拟完交易后我们对数据进行统计：
```
net_rate = (history_capital[-1] - history_capital[0]) / history_capital[0]  # 计算回测结果
print round(net_rate*100, 2), "%"
```
为了让结果更加直观，这里使用matplotlib进行绘图，新建一个绘图工具类：
```
def draw_plt(plt, index, data_list, title='', color="r"):
    plt.subplot(index)
    lable_x = np.arange(len(data_list))
    plt.plot(lable_x, data_list, color=color, linewidth=1.0, linestyle="-")
    plt.xlim(lable_x.min(), lable_x.max() * 1.1)
    plt.ylim(min(data_list) * 0.9, max(data_list) * 1.1)
    plt.title(title)
    plt.grid(True)
```
将结果绘制成图片：
```
plt.figure(figsize=(6, 4), dpi=80)
draw_utils.draw_plt(plt, 111, history_capital, color="r")
plt.show()
```
到此为止，我们已经完成了对策略的回测，在实际的研发过程中，我们可能需要对大量的复杂模型进行回测，下个章节我们将介绍如何使用Python搭建一个完整的回测系统。

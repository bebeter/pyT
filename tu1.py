# -*- coding: utf-8 -*-
import plotly as py
import plotly.graph_objs as go
pyplt = py.offline.plot

# Stacked Bar Chart
trace_1 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0.7252, 0.9912, 0.5347, 0.4436, 0.9911],
    name = '股票投资'
)

trace_2 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0.2072, 0, 0.4081, 0.4955, 0.02],
    name='其它投资'
)

trace_3 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0, 0, 0.037, 0, 0],
    name='债券投资'
)

trace_4 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0.0676, 0.0087, 0.0202, 0.0609, 0.0087],
    name='银行存款'
)


trace_5 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0.2, 0.3, 0.037, 0, 0.2],
    name='债券投资'
)

trace_6 = go.Bar(
    x = ['深证50', '上证50', '西南50', '西北50','华中50'],
    y = [0.0676, 0.0387, 0.0202, 0.0609, 0.0287],
    name='银行存款'
)



trace = [trace_1, trace_2, trace_3, trace_4, trace_5, trace_6]
layout = go.Layout(
    title = '基金资产配置比例图',
    barmode='stack'
)

fig = go.Figure(data = trace, layout = layout)
pyplt(fig, filename='1.html')
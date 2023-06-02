# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
关于青少年心理健康中文研究的可视化，包括年发表文献，年引用量和年下载量的条形图，以及关键词词云图
'''
import pandas as pd
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode

# 绘制词云图
##-------从文件中读出词频------------------
data = pd.read_excel('output/wordsList.xlsx')
# 格式：专业词汇|出现次数

# 过滤count大于10的词
filtered_data = data[data['Count'] > 10]

##-------生成词云-------------------------
cloud = WordCloud()
# 设置词云图
cloud.add('',
          data.values.tolist(),
          shape='triangle-forward',  # 轮廓形状：'circle','cardioid','diamond',
          # 'triangle-forward','triangle','pentagon','star'
          mask_image='./data/背景.jpg',  # 轮廓图，第一次显示可能有问题，刷新即可
          is_draw_out_of_bound=False,  # 允许词云超出画布边界
          word_size_range=[15, 50],  # 字体大小范围
          textstyle_opts=opts.TextStyleOpts(font_family="华文行楷"),
          )

# 设置标题
cloud.set_global_opts(title_opts=opts.TitleOpts(title="中文青少年心理健康研究关键词词云图"))

# render会生成HTML文件。默认是当前目录render.html，也可以指定文件名参数
out_filename = './output/wordcloud_cnki_keywords.html'
cloud.render(out_filename)

print('生成结果文件：' + out_filename)

#绘制条形图

# 读取XLSX文件
data = pd.read_excel('./output/日期统计.xlsx')

# 提取数据
x_data = data['Year'].tolist()
y_data1 = data['Frequency'].tolist()
y_data2 = data['Refer_times'].tolist()
y_data3 = data['Download_times'].tolist()

# 绘制条形图
c = (
    Bar()
    .add_xaxis(x_data)
    .add_yaxis("年发表文献", y_data1)
    .add_yaxis("年被引量", y_data2)
    .add_yaxis("年下载量", y_data3)
    .set_global_opts(
        title_opts=opts.TitleOpts(title=""),
        toolbox_opts=opts.ToolboxOpts(),  # 显示工具栏
        legend_opts=opts.LegendOpts(is_show=True)  # 是否显示图例
    )
    .render("../web/文献发表频次统计条形图.html") #保存结果文件到上级目录中的web文件夹
)
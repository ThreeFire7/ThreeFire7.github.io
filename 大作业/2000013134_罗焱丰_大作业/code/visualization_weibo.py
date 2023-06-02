# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
将爬虫爬取的微博中关于青少年心理健康的讨论分词进行词频统计，并绘制成词云图
'''

import jieba
import jieba.posseg as pseg
import csv
from pyecharts.charts import WordCloud
from pyecharts import options as opts

csv_filename = './output/weibo_texts.csv'
result_filename = './output/微博青少年心理健康词频统计.csv'

# 从文件读取文本
with open(csv_filename, 'r', encoding='utf-8') as txt_file:
    content = txt_file.read()
print('文件读取完成')

# 分词
words = pseg.cut(content)  # pseg.cut返回生成器
print('分词完成')

# 用字典统计每个名词的出现次数
word_dict = {}
print('正在统计所有词中的名词……')
count = 0  # 用于记录已处理的名词数
for one in words:
    # 为便于处理，用w记录本次循环检查的“词”，f记录对应的“词性”
    w = one.word
    f = one.flag

    if len(w) == 1:  # 忽略单字
        continue

    if 'n' in f:  # 如果该词的词性中包含'n'，即这是个名词
        if w in word_dict.keys():  # 如果该词已经在词典中
            word_dict[w] = word_dict[w] + 1
        else:  # 如果该词不在词典中
            word_dict[w] = 1

    # 打印进度
    count = count + 1
    count_quo = int(count / 1000)
    count_mod = count % 1000  # 取模，即做除法得到的余数
    if count_mod == 0:  # 每逢整千的数，打印一次进度
        print('---已处理词数（千）：' + str(count_quo))  # 打印进度信息

print()
print('名词统计完成')

# 删除词频小于五的词
word_dict = {word: freq for word, freq in word_dict.items() if freq >= 5}

# 按词频从大到小排序
sorted_word_dict = dict(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))

# 将词频统计结果写入CSV文件
with open(result_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['词', '词频'])  # 写入标题行
    for word, freq in sorted_word_dict.items():
        writer.writerow([word, freq])  # 写入词和词频

print('词频统计结果已保存为：' + result_filename)

# 绘制词云图
cloud = WordCloud()

# 设置词云图
cloud.add('', list(sorted_word_dict.items())[:90],  # 列表，词和词频
          shape='diamond',  # 轮廓形状：'circle','cardioid','diamond','triangle-forward','triangle','pentagon','star'
          mask_image='./data/背景.jpg',  # 轮廓图，第一次显示可能有问题，刷新即可
          is_draw_out_of_bound=False,  # 允许词云超出画布边界
          word_size_range=[15, 50],  # 字体大小范围
          textstyle_opts=opts.TextStyleOpts(font_family="华文行楷"),
          # 字体：例如，微软雅黑，宋体，华文行楷，Arial
          )

# 设置标题
cloud.set_global_opts(title_opts=opts.TitleOpts(title="微博青少年心理健康词云图"))

# render会生成HTML文件。默认是当前目录render.html，也可以指定文件名参数
out_filename = '../web/微博青少年心理健康词云图.html' #保存结果文件到上级目录中的web文件夹
cloud.render(out_filename)

print('生成结果文件：' + out_filename)
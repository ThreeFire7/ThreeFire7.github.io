# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
预处理cnki的抓取数据，包括词频统计和计算不同年份的年发表量，年被引量和年下载量
'''
import pandas as pd
from collections import Counter

# 1) 导入数据
df = pd.read_excel('output/文献爬取整合数据.xlsx')

# 2) 统计date的词频、refer_times和download_times总和，并输出为xls文件
date_counts = df['date'].value_counts().reset_index()
date_counts.columns = ['Year', 'Frequency']
date_counts['Refer_times'] = df.groupby('date')['refer_times'].sum().values
date_counts['Download_times'] = df.groupby('date')['download_times'].sum().values

# 按照Year从小到大排序
date_counts = date_counts.sort_values('Year')

date_counts.to_excel('output/日期统计.xlsx', index=False)

# 3) 提取abstract列并输出为xls文件（删除空白行）
df['abstract'].dropna().to_excel('output/Abstract.xlsx', index=False)

# 4) 统计keywords中出现的所有词并输出为xls文件（按照count排序，保留Count大于等于50的词）
keywords = '/'.join(df['keywords'].fillna('').astype(str)).split('/')
keywords_counts = dict(Counter(keywords))
words_df = pd.DataFrame.from_dict(keywords_counts, orient='index', columns=['Count'])
words_df.index.name = 'Word'
words_df = words_df.sort_values('Count', ascending=False)  # 按照Count从大到小排序
words_df = words_df.query('Count >= 10')  # 保留Count大于等于10的词
words_df.to_excel('output/wordsList.xlsx')
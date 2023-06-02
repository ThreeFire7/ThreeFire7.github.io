# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
将分别抓取的数据文件合并，去重以及提取量化信息，包括发表年份，引用量和下载量
'''
import os
import pandas as pd

# 1) 合并所有XLSX文件并删除重复行
folder_path = "output/"  # 存放XLSX文件的子文件夹路径
file_names = [
    "青少年焦虑文献爬取.xlsx",
    "青少年心理健康文献爬取.xlsx",
    "青少年抑郁文献爬取.xlsx",
    "学校焦虑文献爬取.xlsx",
    "学校心理健康文献爬取.xlsx",
    "学校抑郁文献爬取.xlsx"
]

dfs = []
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_excel(file_path)
    dfs.append(df)

merged_df = pd.concat(dfs)
merged_df.drop_duplicates(inplace=True)

# 2) 提取date列的前四个字符作为该列的值
merged_df['date'] = merged_df['date'].astype(str).str[:4]

# 3) 提取download_times和refer_times的数字
merged_df['download_times'] = merged_df['download_times'].str[3:-1]
merged_df['refer_times'] = merged_df['refer_times'].str[3:-1]

# 5) 导出数据到新的Excel文件
output_folder = "output"  # 输出文件的子文件夹路径
output_file = "文献爬取整合数据.xlsx"
output_path = os.path.join(output_folder, output_file)

merged_df.to_excel(output_path, index=False, engine='openpyxl', sheet_name='Sheet1')


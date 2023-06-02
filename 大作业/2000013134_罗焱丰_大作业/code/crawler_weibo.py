# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
使用cookies抓取微博中关于青少年心理健康讨论的文字数据
'''

#导入需要的库
from selenium import webdriver
import pandas as pd
import time
# 读取cookies信息
with open('data/my_cookies_weibo.json', 'r') as f:
    cookies = json.load(f)
# 初始化浏览器并添加cookies
driver = webdriver.Chrome()
driver.get('https://weibo.com/')
for cookie in cookies:
    driver.add_cookie(cookie)
# 直接打开微博“青少年心理健康”搜索界面
driver.get('https://s.weibo.com/weibo?q=%E9%9D%92%E5%B0%91%E5%B9%B4%E5%BF%83%E7%90%86%E5%81%A5%E5%BA%B7&Refer=SWeibo_box')
driver.implicitly_wait(10)
# 获取所有微博文本信息
texts = []
while True:
    weibo_list = driver.find_elements_by_xpath('//div[@class="content"]/p[@class="txt"]')
    for weibo in weibo_list:
        # 点击展开按钮
        expand_btn = weibo.find_elements_by_xpath('./a[@action-type="fl_unfold"]')
        if len(expand_btn) > 0:
            expand_btn[0].click()
            time.sleep(1)
        # 获取全部文本信息
        text = weibo.text.replace('收起全文d', '').strip()
        texts.append(text)
    next_page = driver.find_elements_by_xpath('//a[@class="next"]')
    if len(next_page) > 0:
        next_page[0].click()
        time.sleep(2)
    else:
        break
# 保存为csv文件
df = pd.DataFrame({'text': texts})
df.to_csv('./output/weibo_texts.csv', index=False)

# 关闭浏览器
browser.quit()
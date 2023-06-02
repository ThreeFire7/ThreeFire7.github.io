# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
配合手工操作登录微博，获取cookies，保存到本地，以备后续使用
'''
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #用于设置浏览器启动的一些参数
import time

options = Options()

#options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
browser = webdriver.Chrome(options=options)
browser.get('https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=1&url=https%3A%2F%2Fs.weibo.com%2Fweibo%3Fq%3D%25E9%259D%2592%25E5%25B0%2591%25E5%25B9%25B4%25E5%25BF%2583%25E7%2590%2586%25E5%2581%25A5%25E5%25BA%25B7') #可修改替换为其他需要的网站
browser.maximize_window()

input("请用手机扫码登录，然后按回车……")  # 等待用手机扫码登录, 登录后回车即可
# 取cookies并保存成json文件
cookies_dict = browser.get_cookies()
cookies_json = json.dumps(cookies_dict)
print(cookies_json)

# 登录完成后,将cookies保存到本地文件
out_filename = './data/my_cookies_weibo.json'
out_file = open(out_filename, 'w', encoding='utf-8')
out_file.write(cookies_json)
out_file.close()
print('Cookies文件已写入：' + out_filename)

#关闭浏览器
time.sleep(5)
browser.close()

# -*- coding: utf-8 -*-
"""
Created on June 2 2023
@author: 罗焱丰 2000013134
"""
'''
使用requests库，分别以”青少年 心理健康“”青少年 抑郁“”青少年 焦虑“"学校 心理健康””学校 抑郁“”学校 焦虑“作为关键词检索并抓取文献标题，摘要，发表年份
被引量和被下载量等信息。
'''

import requests
from lxml import etree
import os
import time
import xlsxwriter as xw


base_url = 'http://search.cnki.com.cn/Search/ListResult'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    # 'Content-Length': '463'

}


def get_page_text(url, headers, search_word, page_num):
    data = {
        'searchType': ' MulityTermsSearch',
        'ArticleType': '',
        'ReSearch': '',
        'ParamIsNullOrEmpty': ' false',
        'Islegal': ' false',
        'Content': search_word,
        'Theme': '',
        'Title': '',
        'KeyWd': '',
        'Author': '',
        'SearchFund': '',
        'Originate': '',
        'Summary': '',
        'PublishTimeBegin': '',
        'PublishTimeEnd': '',
        'MapNumber': '',
        'Name': '',
        'Issn': '',
        'Cn': '',
        'Unit': '',
        'Public': '',
        'Boss': '',
        'FirstBoss': '',
        'Catalog': '',
        'Reference': '',
        'Speciality': '',
        'Type': '',
        'Subject': '',
        'SpecialityCode': '',
        'UnitCode': '',
        'Year': '',
        'AuthorFilter': '',
        'BossCode': '',
        'Fund': '',
        'Level': '',
        'Elite': '',
        'Organization': '',
        'Order': ' 1',
        'Page': str(page_num),
        'PageIndex': '',
        'ExcludeField': '',
        'ZtCode': '',
        'Smarts': '',
    }

    response = requests.post(url=url, headers=headers, data=data)
    page_text = response.text
    return page_text


def get_abstract(url):
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)
    abstract = tree.xpath('//div[@class="xx_font"]//text()')

    return abstract


def list_to_str(my_list):
    my_str = "".join(my_list)
    return my_str


def parse_page_text(page_text):
    tree = etree.HTML(page_text)
    item_list = tree.xpath('//div[@class="list-item"]')
    page_info = []
    for item in item_list:
        # 标题
        title = list_to_str(item.xpath(
            './p[@class="tit clearfix"]/a[@class="left"]/@title'))
        # 链接
        link = 'https:' +\
            list_to_str(item.xpath(
                './p[@class="tit clearfix"]/a[@class="left"]/@href'))
        # 作者
        author = list_to_str(item.xpath(
            './p[@class="source"]/span[1]/@title'))
        # 导师
        mentor = list_to_str(item.xpath(
            './p[@class="source"]/span[2]/a[1]/text()'))
        # 出版日期
        date = list_to_str(item.xpath(
            './p[@class="source"]/span[last()-1]/text() | ./p[@class="source"]/a[2]/span[1]/text() '))
        # 关键词
        keywords = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_left left"]/a[1]/@data-key'))
        # 摘要
        abstract = list_to_str(get_abstract(url=link))
        # 文献来源
        paper_source = list_to_str(item.xpath(
            './p[@class="source"]/span[last()-2]/text() | ./p[@class="source"]/a[1]/span[1]/text() '))
        # 文献类型
        paper_type = list_to_str(item.xpath(
            './p[@class="source"]/span[last()]/text()'))
        # 下载量
        download_times = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_right right"]/span[@class="time1"]/text()'))
        # 被引量
        refer_times = list_to_str(item.xpath(
            './div[@class="info"]/p[@class="info_right right"]/span[@class="time2"]/text()'))

        item_info = [i.strip() for i in [title, author, mentor,
                     paper_source, paper_type, date, keywords, abstract, download_times, refer_times, link]]
        page_info.append(item_info)
        # print(page_info)
    return page_info


def write_to_excel(workbook, info,  search_word):

    wb = workbook
    worksheet1 = wb.add_worksheet(search_word)  # 创建子表
    worksheet1.activate()  # 激活表

    title = ['title', 'author', 'mentor',
             'paper_source', 'paper_type', 'date', 'keywords', 'abstract', 'download_times', 'refer_times', 'link']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头

    i = 2  # 从第二行开始写入数据
    for j in range(len(info)):
        insert_data = info[j]
        start_pos = 'A' + str(i)
        # print(insert_data)
        worksheet1.write_row(start_pos, insert_data)
        i += 1
    return True


if __name__ == '__main__':

    # 1、创建一个文件夹
    if not os.path.exists('./output'):
        os.mkdir('./output')
    file_name = './output/学校抑郁文献爬取.xlsx' #此参数需要对应调整

    # 2、设置搜索词（为防止搜索词过多爬取中断浪费时间，每次设置一个搜索词，多次爬取所需数据）
    search_words = ['学校 抑郁']
    # 3、创建工作簿
    workbook = xw.Workbook(filename=file_name)

    # 4、获取每个搜索词的文献内容
    for search_word in search_words:
        infos = []
        # 手动获取总页数：250页（不足250页需要手动调整）
        for page_num in range(1, 251):
            print('搜索词：'+search_word+'---正在爬取第【'+str(page_num)+'】页...')
            page_text = get_page_text(
                url=base_url, headers=headers, search_word=search_word, page_num=page_num)
            page_info = parse_page_text(page_text=page_text)
            # 用+合并成一个列表，不是嵌套列表；用append，会形成嵌套列表
            infos += page_info
            time.sleep(5)

        # 5、按照搜索词，依次写入工作簿
        write_to_excel(workbook, infos, search_word)
    # 6、关闭工作簿
    workbook.close()

    print('爬取完成!')
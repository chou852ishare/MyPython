#!/usr/bin/env python
# _*_ coding: utf-8 -*-

__author__ = 'ziye'

from bs4 import BeautifulSoup
from selenium import webdriver
# import selenium.webdriver.support.ui as ui
import os

# set work directory
os.chdir('./output/test/')

# open the browser
browser = webdriver.Firefox()  # 打开Firefox浏览器
# wait = ui.WebDriverWait(browser,10) # 设定最长等待加载时间为10秒
browser.get("http://xwb100.cn/search.php")  # 打开网址


# set up the crawler
def crawler(page_num, file_name):
    try:
        # click the javascript button
        page_location = "//a[@href='javascript:nextpage_dosubmit(%d)']" %page_num
        browser.find_element_by_xpath(page_location).click()
        # parse the html
        soup = BeautifulSoup(browser.page_source) #, from_encoding = 'gb2312')
        articles = soup.find_all('tr')[1:]
        # write down info
        for i in articles:
            td = i.find_all('td')
            num = td[0].text
            title = td[1].text
            link = td[1].a['href']
            author = td[2].text
            date = td[3].text
            views = td[4].text
            likes = td[5].text
            record = num + '\t' + title+ '\t' + link+ '\t' + author+ '\t' + date+ '\t' + views+ '\t' + likes
            with open(file_name, 'a') as p: # '''Note''': Append mode, run only once!
                p.write(record.encode('utf-8')+"\n") ## !!encode here to utf-8 to avoid encoding error.
    except:
        pass

# crawl all ranks
for page_num in range(1, 11):
    print page_num
    crawler(page_num, 'xwb100_all.txt')
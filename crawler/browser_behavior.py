#!/usr/bin/env python
# _*_ coding: utf-8 -*-

__author__ = 'ziye'

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
# from selenium.common.exceptions import
import os

# set work directory
# os.chdir('./output/test/')

# set virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

# open the browser
browser = webdriver.Firefox()
# open the website
query_page = 'http://www.3533.com/phone/'
browser.get(query_page)


# combinations of model keys
def combine(keymodel, separator):
    if keymodel.__contains__(separator):
        key0 = keymodel.split(separator)[0]
        key1 = keymodel.split(separator)[1]
        if len(key0) > len(key1):
            return [keymodel, key0]
        else:
            return [keymodel, key1]
    else:
        return [keymodel]


# set up the crawler
# steps to get price and info. for a phone model
# 1. fill in phone brand and choose the first autocomplete
# 2. fill in phone model and choose the first autocomplete
# 3. get href of /brand/model/canshu.htm
# 4. parse web with href
def crawler(keybrand, keymodel, file_name):
    find_phone = False
    keys = combine(keymodel, '-')
    for key in keys:
        # 1. fill in phone brand and select the first autocomplete
        try:
            brand = browser.find_element_by_class_name('find_model_brand')
        except:
            return
        brand.clear()
        brand.send_keys(keybrand.decode('utf-8'))
        # click the first autocomplete after at most 2s
        autobrand = "//div[@id='find_model_box']/div/div[4]/a[1]"
        try:
            WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, autobrand)))
            elebrand = browser.find_element_by_xpath(autobrand)
            elebrand.click()
            branden = elebrand.get_attribute('en').lower()
        except:
            branden = keybrand.lower()

        # 2. fill in phone model and select the first autocomplete
        model = browser.find_element_by_class_name('find_model_mobile')
        model.clear()
        model.send_keys(key.decode('utf-8'))
        # if brand name is not correct, a popup dialog alerts. then quit
        flag_alert = False
        try:
            alert = browser.switch_to.alert
            while alert.text:
                flag_alert = True
                alert.dismiss()
                alert = browser.switch_to.alert
        except NoAlertPresentException, e:
            pass
        if flag_alert:
            return
        # click the first autocomplete after at most 2s
        automodel = "//div[@id='find_model_box']/div/div[5]/a[1]"
        try:
            WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, automodel)))
            elemodel = browser.find_element_by_xpath(automodel)
            if elemodel:
                elemodel.click()
                modelen = elemodel.get_attribute('en').lower()
        except:
            modelen = key.lower()

        # 3. get href of /brand/model/canshu.htm
        url = 'http://www.3533.com/' + branden + '/' + modelen + '/canshu.htm'
        try:
            browser.get(url)
            if u'错误' in browser.title:
                browser.back()
            else:
                find_phone = True
                break
        except:
            continue
    if not find_phone:
        return

    # 4. parse the canshu html
    soup = BeautifulSoup(browser.page_source)
    mainparam = soup.find(class_='mainparam')
    tbody = soup.find('tbody')
    browser.back()
    # write down info
    try:
        price = mainparam.find(class_='price').span.text.strip().replace('\n', '')
    except:
        price = u'-1'
    try:
        year = mainparam.find('span', text=u'上市年份：').next_sibling.text.strip().replace('\n', '')
    except:
        year = u'-1'
    try:
        ram = mainparam.find('span', text=u'机身内存：').next_sibling.text.strip().replace('\n', '')
    except:
        ram = u'-1'
    try:
        battery = mainparam.find('span', text=u'电池容量：').next_sibling.text.strip().replace('\n', '')
    except:
        battery = u'-1'
    try:
        screen = mainparam.find('span', text=u'主屏尺寸：').next_sibling.get_text('|').strip().replace('\n', '')
        try:
            screen_size = screen.split('|')[0]
        except:
            screen_size = u'-1'
        try:
            screen_pixel = screen.split('|')[1]
        except:
            screen_pixel = u'-1'
    except:
        screen_size = u'-1'
        screen_pixel = u'-1'
    try:
        camera_pixel = mainparam.find('span', text=u'摄像头像素：').next_sibling.text.strip().replace('\n', '').replace(',', '_')
    except:
        camera_pixel = u'-1'
    try:
        osp = mainparam.find('span', text=u'操作系统：').next_sibling.text.strip().replace('\n', '')
    except:
        osp = u'-1'
    try:
        cpu = tbody.find('span', text=u'CPU频率：').next_sibling.text.strip().replace('\n', '')
        try:
            cpu_freq = cpu.split(' ')[0]
        except:
            cpu_freq = u'-1'
        try:
            cpu_manu = ''.join(cpu.split(' ')[1:])
        except:
            cpu_manu = u'-1'
        try:
            cpu_core = tbody.find('span', text=u'CPU核心数：').next_sibling.text.strip().replace('\n', '')
        except:
            cpu_core = u'1'
    except:
        cpu_freq = u'-1'
        cpu_manu = u'-1'
        cpu_core = u'-1'

    # write
    phone_info = [keybrand+'_'+keymodel, branden+'_'+modelen, price, year, ram, battery, screen_size, screen_pixel, camera_pixel, osp, cpu_freq, cpu_manu, cpu_core]
    output = ','.join(phone_info)
    with open(file_name, 'a') as p:
                p.write(output.encode('utf-8')+"\n")

# crawl all ranks
# read phone brands and models
with open('./phone_brand', 'r') as rf:
    for line in rf.readlines():
        phone = line.replace('\n', '').split(',')
        print phone
        crawler(phone[0], phone[1], './output/test/phone_info')
browser.quit()
# display.stop()
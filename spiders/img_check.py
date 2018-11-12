# -*- coding: utf-8 -*-
# @File  : img_check.py
# @Author: KingJX
# @Date  : 2018/10/29 15:53
""""""
import os

from io import BytesIO

import pymysql
import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from urllib.request import ProxyHandler, build_opener
from lxml import etree
import time
import random

from codes import *
from compare_helper import get_compare

chrome_options = webdriver.ChromeOptions()

browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 10)



# pro = requests.get('http://127.0.0.1:5555/random', headers=headers)
# proxy = pro.content.decode('utf-8')
# print(proxy)
#
# proxy_handler = ProxyHandler({
#     'http': 'http://' + proxy,
#     'https': 'https://' + proxy
# })
# headers = {
#         "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
#     }
# opener = build_opener(proxy_handler)
# response = opener.open('http://httpbin.org/get')
# print(response.read().decode('utf-8'))
#

def get_page():
    url = 'http://www.1kkk.com/'
    browser.get(url)
    html = browser.page_source
    return html


def open_login():
    # 打开登录界面, 并输入账号密码
    login_a = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.header_login.hover')))
    login_a.click()
    time.sleep(1)
    input_name = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@name="txt_name"]')))
    input_pwd = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@name="txt_password"]')))
    input_name.clear()
    input_pwd.clear()
    input_name.send_keys(MAIL_NAME)
    input_pwd.send_keys(MAIL_PWD)
    time.sleep(5)



def get_big_html_img():
    # 截取屏幕大图
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def get_position():
    img_s = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="rotate-background"]')))
    for img in img_s:
        loc = img.location
        size = img.size
        x1 = loc['x']
        y1 = loc['y']
        x2 = loc['x'] + size['width']
        y2 = loc['y'] + size['height']
        yield x1, y1, x2, y2


def parse_html(html):
    etree.html = etree.HTML(html)
    x1, x2, x3, x4 = get_position()
    all_img = (x1, x2, x3, x4)
    print(all_img)
    i = 0
    for imgs in all_img:
        fun1(imgs, i)
        i += 1


def fun1(imgs, i):
    checked = True
    j = 0
    while checked:
        print('*****************')
        print(imgs)
        screen_shot = get_big_html_img()
        print(screen_shot)
        crop_img = screen_shot.crop(imgs)
        crop_img.save('./check_img/1.png')
        img1 = os.listdir('./little_img')
        for img in img1:
            img11 = './little_img/' + img
            compare = get_compare('./check_img/1.png', img11)
            print(compare)
            if compare > 75:
                print('***********************************************************************************')
                return None
        img_s = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="rotate-background"]')))
        img_s[i].click()


def get_big_img(name):
    """
    获取大图
    :param name:
    :return:
    """
    url = 'http://www.1kkk.com/image3.ashx?%d' % name
    with open('./img_roll/%d.png' % name, 'wb')as f:
        response = requests.get(url)
        f.write(response.content)


def get_little_img():
    """
    获取小图
    :return:
    """
    img_list = os.listdir('./img_roll')
    print(img_list)
    height = 76
    width = 76
    for img_name in img_list:
        with open('./img_roll/%s' % img_name, 'rb')as f:
            imgs = f.read()
        for i in range(4):
            img = Image.open(BytesIO(imgs))
            crop_img = img.crop((i * height, i * width, (i + 1) * height, (i + 1) * width))
            crop_img.save('./little_img/%s-%d.png' % (img_list.index(img_name), i))
            print(img_list.index(img_name), '-', i)


def main():
    html = get_page()
    open_login()
    get_big_html_img()
    get_position()
    parse_html(html)
    # 获取大图
    # for i in range(200):
    #     get_big_img(i)
    #     print('正在获取第%i个图片' % i)
    # print('图片获取完毕')
    # # 获取小图
    # get_little_img()


if __name__ == '__main__':
    main()

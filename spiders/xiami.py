# -*- coding: utf-8 -*-
# @File  : xiami.py
# @Author: KingJX
# @Date  : 2018/10/25 17:43
""""""
from urllib import parse

import json
import requests
import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
import time
import random

chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 10)


def str2url(s):
    num_loc = s.find('h')
    rows = int(s[0:num_loc])
    strlen = len(s) - num_loc
    cols = int(strlen/rows)
    right_rows = strlen % rows
    new_s = list(s[num_loc:])
    output = ''
    for i in range(len(new_s)):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
        output += new_s[int(p)]
    return parse.unquote(output).replace('^', '0')


def get_page():
    url = 'https://www.xiami.com/chart'
    browser.get(url)
    for i in range(4):
        str1 = 'var step = document.body.scrollHeight / 4;window.scrollTo(0, step * %d)' % i
        browser.execute_script(str1)
        num = random.randint(1, 3)
        time.sleep(num)
    page_source = browser.page_source
    return page_source


def parse_page(page_source):
    etree_html = etree.HTML(page_source)
    all_music = etree_html.xpath('//div[@id="chart"]/table/*')
    musics = []
    for music in all_music:
        music_url_1 = music.xpath('./@data-mp3')[0]
        name = music.xpath('./td[@class="songblock"]/div/div[@class="info"]/p/strong/a/text()')[0]
        music_url = str2url(music_url_1)
        print(music_url)
        with open('./mp3/%s.mp3' % name, 'wb')as f:
            response = requests.get(music_url)
            f.write(response.content)

    return musics


def main():
    page_source = get_page()
    parse_page(page_source)


if __name__ == '__main__':
    main()

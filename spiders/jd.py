# -*- coding: utf-8 -*-
# @File  : chrome.py
# @Author: KingJX
# @Date  : 2018/10/25 10:04
""""""
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
# chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 10)
KEYWORD = '笔记本'


def create_clothes_info(cursor, db, g_id, img, price, name, shop, commit):
    sql = 'insert into notebook(g_id, img, price, name, shop, commit_num) value ("%d","%s","%f","%s","%s","%s")' % (
        g_id, img, price, name, shop, commit)
    try:
        cursor.execute(sql)
        print('***********')
        db.commit()
    except:
        print('-----------')
        db.rollback()


def get_page(page):
    if page == 1:
        url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % quote(KEYWORD)
        browser.get(url)
    if page > 1:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage span.p-skip input.input-txt')))
        input.clear()
        input.send_keys(page)

        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn.btn-default')))
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_topPage span.fp-text b'), str(page)))
    for i in range(4):
        str1 = 'var step = document.body.scrollHeight / 4;window.scrollTo(0, step * %d)' % i
        browser.execute_script(str1)
        num = random.randint(1, 3)
        time.sleep(num)
    page_source = browser.page_source
    return page_source


def parse_page(cursor, db, page_source):
    etree_html = etree.HTML(page_source)
    # print(etree_html)
    all = etree_html.xpath('.//div[@class="gl-warp clearfix"]/*')
    for good in all:
        arr = good.xpath('.//div[@class="p-name p-name-type-2"]//a/em/text()')
        name = ''
        for it in arr:
            name += it
        g_id = int(good.xpath('./@data-sku')[0])
        img = good.xpath('.//div[@class="p-img"]/a/img/@src')
        price = float(good.xpath('.//div[@class="p-price"]//i/text()')[0])
        name = name
        shop = good.xpath('.//div[@class="p-shop"]//a/@title')
        commit = good.xpath('.//div[@class="p-commit"]/strong/a/text()')
        create_clothes_info(cursor, db, g_id, img, price, name, shop, commit)


def main():
    db = pymysql.connect(host='localhost', user='root', password='root', database='jd_notebook', port=3306)
    cursor = db.cursor()
    for page in range(100):
        page_source = get_page(page + 1)
        parse_page(cursor, db, page_source)


if __name__ == '__main__':
    main()

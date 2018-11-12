# -*- coding: utf-8 -*-
# @File  : mogujie_all.py
# @Author: KingJX
# @Date  : 2018/10/24 19:01
""""""
import pymysql
import requests
import json

num = 1


def create_clothes_info(cursor, db, clothes_id, title, img, org_price, sale, cfav, price):
    sql = 'insert into clothes_all(clothes_id, title,img,org_price,sale,cfav,price) value ("%s","%s","%s","%f","%d","%d","%f")' % (
        clothes_id, title, img, org_price, sale, cfav, price)
    global num
    num += 1
    print(num)
    try:

        cursor.execute(sql)
        print('***********')
        db.commit()
    except:
        print('-----------')
        db.rollback()


def create_kind(cursor, db, pid, type_name):
    sql1 = 'insert into kind(pid, type_name) value ("%d","%s")' % (pid, type_name)
    # sql2 = 'insert into clothes_all() value ("%d")' % (i+1)
    try:
        cursor.execute(sql1)
        # cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('GBK')
        return text
    return None


def get_clothes_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def get_pid(cursor, db, html):
    html_pid = html[5:-1]
    json_pid = json.loads(html_pid)
    pid = []
    type_name = []
    for i in range(len(json_pid['data']['110119']['list'])):
        p_id = int(json_pid['data']['110119']['list'][i]['categoryDetailPid'])
        name = json_pid['data']['110119']['list'][i]['categoryName']
        pid.append(p_id)
        type_name.append(name)
        create_kind(cursor, db, p_id, name)
    return pid


def get_kind_fcid(pids, i):
    fcid_url = 'https://mce.mogujie.com/jsonp/makeup/3?pid=%s' % pids[i]
    html_fcid = get_one_page(fcid_url)[5:-1]
    json_fcid = json.loads(html_fcid)
    fcid_str = json_fcid['data']['topic1']['list'][0]['link']
    fcid = fcid_str.split('?')[0].split('/')[-1]
    return fcid


def get_clothes(cursor, db, fcid):
    j = 1
    while True:
        clothes_url = 'https://list.mogujie.com/search?cKey=15&page=%dfcid=%s' % (j, fcid)
        html_clothes = get_clothes_page(clothes_url)
        json_clothes = json.loads(html_clothes)
        for i in range(len(json_clothes['result']['wall']['docs'])):
            clothes_id = json_clothes['result']['wall']['docs'][i]['tradeItemId']
            img = json_clothes['result']['wall']['docs'][i]['img']
            title = json_clothes['result']['wall']['docs'][i]['title']
            org_price = float(json_clothes['result']['wall']['docs'][i]['orgPrice'])
            sale = int(json_clothes['result']['wall']['docs'][i]['sale'])
            cfav = int(json_clothes['result']['wall']['docs'][i]['cfav'])
            price = float(json_clothes['result']['wall']['docs'][i]['price'])
            create_clothes_info(cursor, db, clothes_id, title, img, org_price, sale, cfav, price)
        j += 1
        if json_clothes['result']['wall']['isEnd']:
            return


def main():
    db = pymysql.connect(host='localhost', user='root', password='root', database='mogujie_all', port=3306)
    cursor = db.cursor()
    url = 'https://mce.mogucdn.com/jsonp/multiget/3?pids=110119'
    html = get_one_page(url)
    pids = get_pid(cursor, db, html)
    for i in range(len(pids)):
        fcid = get_kind_fcid(pids, i)
        for j in range(len(fcid)):
            get_clothes(cursor, db, fcid)
            pass


if __name__ == '__main__':
    main()

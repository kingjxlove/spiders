from bs4 import BeautifulSoup
import requests
import json
import pymysql


def connect_sql():
    db = pymysql.connect(host='localhost', user='root', password='root', database='test', port=3306)
    cursor = db.cursor()

    # sql = "insert into python (job_title) values ('%s')" % salary


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    job_title = soup.select('.name a .job-title')
    money = soup.select('.name a .red')
    company = soup.select('.company-text .name a')
    address_years_degree = soup.select('.info-primary p')
    time = soup.select('.info-publis p')

    for i in range(len(job_title)):
        job_info = {
            'job_title': list(job_title[i].stripped_strings)[0],
            'salary': list(money[i].stripped_strings)[0],
            'company': list(company[i].stripped_strings)[0],
            'address': list(address_years_degree[i].stripped_strings)[0],
            'years': list(address_years_degree[i].stripped_strings)[1],
            'degree': list(address_years_degree[i].stripped_strings)[2],
            'time': list(time[i])[0]
        }
        keep(job_info)
        print(job_info)


def keep(info):
    with open('python.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(info, ensure_ascii=False) + '\n')


def main():
    page = 1
    url = "https://www.zhipin.com/c100010000-p100109/?page=%d&ka=page-%d" % (page, page)
    for i in range(10):
        url = "https://www.zhipin.com/c100010000-p100109/?page=%d&ka=page-%d" % (i + 1, i + 1)
        html = get_one_page(url)
        parse_soup(html)


if __name__ == '__main__':
    main()

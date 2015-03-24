from datetime import datetime
import json
import re
import urllib

import requests
from bs4 import BeautifulSoup

from monitor import conn, col


def interval_job(key, tag, data_list):
    for data in data_list:
        record = col.Record.find_one({'store': key, 'tag': tag, 'name': data[0]})
        if not record:
            record = conn.Record()

        record['store'] = key
        record['name'] = data[0]
        record['model'] = data[1]
        record['price'] = data[2]
        record['note'] = data[3]
        record['url'] = data[4]
        record['update'] = datetime.utcnow()
        record['tag'] = tag
        record.save()


def __get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)


def dick_smith_job(urls, name_filter):
    data = []
    for url in urls:
        for item in __get_soup(url).findAll('li', attrs={'class': 'item'}):
            name = item.h3.a.text

            if name_filter(name):
                txt = item.find('div', 'savtxt')
                model = item.find('span', 'product-code').text
                price = item.find('span', 'price').text.replace(',', '')
                note = txt.span.text if txt else u''
                link = item.h3.a.get('href')

                data.append([name, model, price, note, link])

    return data
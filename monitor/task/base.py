from datetime import datetime

import requests
from bs4 import BeautifulSoup

from monitor import conn, col


class JobConfig:
    def __init__(self, store, urls, keys, wipe, tag):
        self.store = store
        self.urls = urls
        self.keys = keys
        self.wipe = wipe
        self.tag = tag


def name_filter(name, job_conf):
    if name and job_conf:
        name = name.lower()
        return all(k in name for k in job_conf.keys) and (not any(w in name for w in job_conf.wipe))
    else:
        return False


def interval_job(job_conf, data_gen):
    for data in data_gen(job_conf):
        record = col.Record.find_one({'store': job_conf.store, 'tag': job_conf.tag, 'name': data[0]}) or conn.Record()

        record['store'] = job_conf.store
        record['name'] = data[0]
        record['model'] = data[1]
        record['price'] = data[2]
        record['note'] = data[3]
        record['url'] = data[4]
        record['update'] = datetime.utcnow()
        record['tag'] = job_conf.tag
        record.save()


def __get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text)


def dick_smith_data_gen(job_conf):
    data = []
    for url in job_conf.urls:
        for item in __get_soup(url).findAll('li', attrs={'class': 'item'}):
            name = item.h3.a.text

            if name_filter(name, job_conf):
                txt = item.find('div', 'save-txt')
                model = item.find('span', 'product-code').text
                price = item.find('span', 'price').text.replace(',', '')
                note = txt.text.strip() if txt else u''
                link = item.h3.a.get('href')

                data.append([name, model, price, note, link])

    return data

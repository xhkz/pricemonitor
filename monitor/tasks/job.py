from datetime import datetime
from bs4 import BeautifulSoup
import requests

from monitor import sched, conn, app, col


DS_KEY = u'Dick Smith'
DS_URL = "http://www.dicksmith.com.au/apple-mac"

def interval_job(key, data_list):
    col.remove({'store': key})
    for data in data_list:
        record = conn.Record()
        record['store'] = key
        record['name'] = data[0]
        record['model'] = data[1]
        record['price'] = data[2]
        record['note'] = data[3]
        record['url'] = data[4]
        record['update'] = datetime.utcnow()
        record.save()


@sched.scheduled_job('interval', seconds=app.config['TASK_INTERVAL'])
def dick_smith_job():
    r = requests.get(DS_URL)
    soup = BeautifulSoup(r.text)
    items = soup.findAll('li', attrs={'class': 'item'})

    data = []

    for item in items:
        name = item.h3.a.text

        if name and name.lower().find('mac') != -1:
            txt = item.find('div', 'savtxt')
            model = item.find('span', 'product-code').text
            price = item.find('span', 'price').text
            note = txt.span.text if txt else u''
            link = item.h3.a.get('href')

            data.append([name, model, price, note, link])

    interval_job(DS_KEY, data)
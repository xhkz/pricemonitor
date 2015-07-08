import os
from datetime import datetime

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from mongokit import Connection, Document

app = Flask(__name__)
app.config.from_pyfile('config.py')

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

sched = BackgroundScheduler(executors=executors, logger=app.logger)
sched.start()

conn = Connection(os.environ['OPENSHIFT_MONGODB_DB_URL'])
col = conn['pricedb'].pricedata

import views.main
import task.jobs


@conn.register
class Record(Document):
    __collection__ = 'pricedata'
    __database__ = 'pricedb'

    structure = {
        'store': unicode,
        'name': unicode,
        'model': unicode,
        'price': unicode,
        'note': unicode,
        'update': datetime,
        'url': unicode,
        'tag': unicode
    }

    required_fields = ['store', 'name', 'price', 'url', 'tag']

    default_values = {
        'update': datetime.utcnow()
    }

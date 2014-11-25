from datetime import datetime

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from mongokit import Connection, Document


app = Flask(__name__)
app.config.from_pyfile('config.py')

sched = BackgroundScheduler(logger=app.logger)
sched.start()

conn = Connection(app.config['MONGODB_URI'])
col = conn['pricedb'].pricedata

import views.main
import tasks.job


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
        'url': unicode
    }

    required_fields = ['store', 'name', 'price', 'url']

    default_values = {
        'update': datetime.utcnow()
    }
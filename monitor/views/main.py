from flask import render_template
import pymongo
import pytz

from monitor import app, col


@app.route('/')
@app.route('/macbook_pro')
def macbook_pro():
    return render_template('main.html', items=__fetch_data('.*macbook.*pro.*'))


def __fetch_data(keyword):
    items = []
    for r in col.Record.find({'name': {'$regex': keyword, '$options': 'i'}}).sort('store', pymongo.ASCENDING):
        r['update'] = r['update'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Melbourne'))
        items.append(r)

    return items

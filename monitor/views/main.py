from flask import render_template
import pymongo
import pytz

from monitor import app, col


@app.route('/')
@app.route('/macbook_pro')
def macbook_pro():
    return render_template('main.html', items=__fetch_data('.*macbook.*pro.*'))


@app.route('/mac_pro')
def mac_pro():
    return render_template('main.html', items=__fetch_data('.*mac pro.*'))


@app.route('/macbook_air')
def macbook_air():
    return render_template('main.html', items=__fetch_data('.*air.*'))


@app.route('/imac')
def imac():
    return render_template('main.html', items=__fetch_data('.*imac.*'))


@app.route('/mini')
def mini():
    return render_template('main.html', items=__fetch_data('.*mini.*'))


def __fetch_data(keyword):
    items = []
    for r in col.Record.find({'name': {'$regex': keyword, '$options': 'i'}}).sort('store', pymongo.ASCENDING):
        r['update'] = r['update'].replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Australia/Melbourne'))
        items.append(r)

    return items
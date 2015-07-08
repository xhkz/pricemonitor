from monitor import sched, app
from base import *

MAC_TAG = u'MAC'
MAC_KEYS = ['mac']
MAC_WIPES = ['care']


@sched.scheduled_job('interval', minutes=app.config['TASK_INT_MIN'])
def dick_smith_job():
    store = u'Dick Smith'

    interval_job(JobConfig(store, ['http://www.dicksmith.com.au/apple-mac'], MAC_KEYS, MAC_WIPES, MAC_TAG),
                 dick_smith_data_gen)

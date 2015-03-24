from monitor import sched, app
import job


TAG = u'MAC'


def name_filter(name):
    if not name:
        return False

    return name.lower().find('mac') != -1


@sched.scheduled_job('interval', seconds=app.config['TASK_INTERVAL'])
def mac_dick_smith_job():
    key = u'Dick Smith'
    urls = ['http://www.dicksmith.com.au/apple-mac']

    job.interval_job(key, TAG, job.dick_smith_job(urls, name_filter))
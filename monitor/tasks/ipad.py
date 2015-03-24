from monitor import sched, app
import job


TAG = u'IPAD'


def name_filter(name):
    if not name:
        return False

    l_name = name.lower()
    return l_name.find('ipad') != -1 and l_name.find('case') == -1 and l_name.find('cover') == -1 \
           and l_name.find('care') == -1


@sched.scheduled_job('interval', seconds=app.config['TASK_INTERVAL'])
def ipad_dick_smith_job():
    key = u'Dick Smith'
    urls = ['http://www.dicksmith.com.au/apple-ipad']

    job.interval_job(key, TAG, job.dick_smith_job(urls, name_filter))
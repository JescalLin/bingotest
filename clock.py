from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=29)
def timed_job_awake_your_app():
    print('awake app every 29 minutes.')
    url = 'https://bingoflask.herokuapp.com/'
    r = requests.get(url)
    print("--> r.content")
    print(r.content)

sched.start()
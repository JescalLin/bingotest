from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time
from datetime import datetime,timezone,timedelta


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=29)
def timed_job_awake_your_app():


    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    start_time = dt2.strptime(str(dt2.now().date()) + '7:00', '%Y-%m-%d%H:%M')
    end_time = dt2.strptime(str(dt2.now().date()) + '23:59', '%Y-%m-%d%H:%M')
    now_time = dt2.now()
    print(now_time)
    if start_time < now_time < end_time:
        print('awake app every 29 minutes.')
        url = 'https://bingoflask.herokuapp.com/'
        r = requests.get(url)
        print("--> r.content")
        print(r.content)
    else:
        url = 'https://bingoflask.herokuapp.com/'
        r = requests.get(url)

sched.start()
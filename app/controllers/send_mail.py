import sched
import time

scheduler = sched.scheduler()

def saytime():
    print(time.ctime())
    scheduler.enter(delay=5,priority=0,action=saytime)

saytime()

try:
    scheduler.run(blocking=False)
except KeyboardInterrupt:
    print('parado')
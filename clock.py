from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from run import runProgram
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def execute_program():
    q.enqueue(runProgram())

sched.add_job(execute_program, trigger='cron', hour='6',minute='35')

sched.add_job(execute_program, trigger='cron', hour='10')
sched.add_job(execute_program, trigger='cron', hour='14')
sched.add_job(execute_program, trigger='cron', hour='18')
sched.start()
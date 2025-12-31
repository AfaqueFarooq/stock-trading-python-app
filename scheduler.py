import schedule
from datetime import datetime
import time
from script import run_stock_job

def basic_job():
    print("Job Executed at", datetime.now())

schedule.every().minute.do(basic_job)

schedule.every().minute.do(run_stock_job)

while True:
    schedule.run_pending()
    time.sleep(1)
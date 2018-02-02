import time
from celery_app import cel
import subprocess
@cel.task
def add(x,y):
    time.sleep(5)
    return x+y

@cel.task
def executepuppeteer(name):
    time.sleep(5)
    process = subprocess.Popen("cd %s && node %s "%("/Users/i072687/Desktop/cases",name),stdout=subprocess.PIPE, shell=True)
    process.wait()
    return {"status":"task completed","result":42, "log_path":"1233"}
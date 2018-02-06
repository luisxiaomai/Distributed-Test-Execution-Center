import time
from celery_app import cel
import subprocess
@cel.task
def add(x,y):
    time.sleep(5)
    return x+y

@cel.task(bind=True)
def executepuppeteer(self,caseList):
    print(caseList)
    time.sleep(5)
    for case in caseList:
        process = subprocess.Popen("cd %s && node %s "%("/Users/i072687/Desktop/cases",case),stdout=subprocess.PIPE, shell=True)
        process.wait()
        self.update_state(state='PROGRESS', meta={'current':caseList.index(case)+1,'total':len(caseList)})
    return {"status":"task completed","result":42, "log_path":"1233"}
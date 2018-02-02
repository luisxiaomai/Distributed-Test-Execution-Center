import time
from celery_app import cel

@cel.task
def multiply(x,y):
    time.sleep(2)
    return x*y
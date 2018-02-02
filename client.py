from celery_app import task1
from celery_app import task2

task1.add.apply_async(args=[2,8])
task2.multiply.apply_async(args=[3,7])

print("hello, world")
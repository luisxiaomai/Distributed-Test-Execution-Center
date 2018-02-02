BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' 

CELERY_IMPORTS = ( 
'celery_app.task1',
'celery_app.task2'
)
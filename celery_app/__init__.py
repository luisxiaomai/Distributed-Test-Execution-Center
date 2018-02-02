from celery import Celery

cel = Celery("executeTestCase")
cel.config_from_object('celery_app.celeryconfig')
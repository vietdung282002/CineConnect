from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CineConnect.settings')

app = Celery('CineConnect')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
import ssl

# ssl_context = ssl.create_default_context()
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE

# app.conf.broker_use_ssl = {
#     'ssl_cert_reqs': ssl.CERT_NONE
# }

# app.conf.result_backend_use_ssl = {
#     'ssl_cert_reqs': ssl.CERT_NONE
# }

# app.conf.beat_schedule = {
#     'run-task-every-1-minutes': {
#         'task': 'webjob.tasks.test',  # Đường dẫn tới hàm bạn muốn chạy
#         'schedule': crontab(minute='*/1'),  # Chạy mỗi 5 phút
#     },
# }
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

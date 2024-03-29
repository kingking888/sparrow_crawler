from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparrow_crawler.settings')
# import pdb; pdb.set_trace()
# try:
#     os.environ['DJANGO_SETTINGS_MODULE']
# except KeyError:
#     # 出错了，设置为测试
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hg_backend.test_sparrow_settings')

# try:
#     setting = os.environ['DJANGO_SETTINGS_MODULE']
#     print(setting)
# except:
#     pass
app = Celery('sparrow_crawler')
# import pdb; pdb.set_trace()
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Load task modules from all registered Django app configs.
# import pdb; pdb.set_trace()
app.autodiscover_tasks()
# 注册command
# import pdb; pdb.set_trace()
app.autodiscover_tasks(packages=["celery_tasks"], related_name='crawler_products_tasks')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
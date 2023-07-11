from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleExampleTask(self):
    try:
        print(f"*******Example Task has started ********")
    except Exception as e:
        return str(e)
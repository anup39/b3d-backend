from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .create_bands import handleCreateBandsNormal


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleExampleTask(self):
    try:
        print(f"*******Example Task has started ********")
    except Exception as e:
        return str(e)


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleCreateBandsNormal_(self,file_path,raster_id,output_folder):
    try:
        result = handleCreateBandsNormal(file_path,raster_id,output_folder)
        return result
        
    except Exception as e:
        return str(e)
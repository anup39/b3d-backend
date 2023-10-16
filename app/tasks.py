from __future__ import absolute_import, unicode_literals
from celery import shared_task
import subprocess



@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleExampleTask(self):
    try:
        print(f"*******Example Task has started ********")
    except Exception as e:
        return str(e)

@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleCreateBands(self,file_path , id):
    try:
        print(f"*******Create Bands from single Tif ********")
        command_red = f"gdal_translate -b 1 -a_nodata 0 media/{file_path} rasters/{id}_red.tif"
        command_green = f"gdal_translate -b 2 -a_nodata 0 media/{file_path} rasters/{id}_green.tif"
        command_blue = f"gdal_translate -b 3 -a_nodata 0 media/{file_path}  rasters/{id}_blue.tif"

        subprocess.call(command_red, shell=True)
        subprocess.call(command_green, shell=True)
        subprocess.call(command_blue, shell=True)


    except Exception as e:
        return str(e)
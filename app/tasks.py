from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .create_bands import handleCreateBandsNormal
from .process_all_geodata import process_all_geodata


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleExampleTask(self):
    try:
        print(f"*******Example Task has started ********")
    except Exception as e:
        return str(e)


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def handleCreateBandsNormal_(self, file_path, raster_id, output_folder, model):
    try:
        result = handleCreateBandsNormal(
            file_path, raster_id, output_folder, model)
        return result

    except Exception as e:
        return str(e)


@shared_task(bind=True, max_retries=3, soft_time_limit=2000)
def process_all_geodata_(self, df, filtered_result, request, standard_categories, sub_categories, categories, client, project, user, task_id):
    try:
        result = process_all_geodata(
            df, filtered_result, request, standard_categories, sub_categories, categories, client, project, user, task_id)
        return result

    except Exception as e:
        return str(e)

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .create_bands import handleCreateBandsNormal
from .process_all_geodata import process_all_geodata
from .models import MeasuringFileUpload, Client, Category, StandardCategory, SubCategory, Project, User
import geopandas as gpd


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
def process_all_geodata_(self, file_path, filtered_result, client_id, project_id, user_id, id):
    try:
        client = Client.objects.get(id=client_id)
        project = Project.objects.get(id=project_id)
        user = User.objects.get(id=user_id)
        categories = {
            category.id: category for category in Category.objects.all()}
        standard_categories = {
            standard_category.id: standard_category for standard_category in StandardCategory.objects.all()}
        sub_categories = {
            sub_category.id: sub_category for sub_category in SubCategory.objects.all()}
        measuring_upload = MeasuringFileUpload.objects.get(id=id)
        task_id = self.request.id
        df = gpd.read_file(file_path)
        result = process_all_geodata(
            df, filtered_result, standard_categories, sub_categories, categories, client, project, user, id, task_id)
        if result == 'Completed':  # replace 'expected_result' with the actual value you're expecting
            measuring_upload.status = 'Completed'
            measuring_upload.progress = 100
            measuring_upload.task_id = task_id
            measuring_upload.total_features = len(df)
            measuring_upload.save()

    except Exception as e:
        return str(e)

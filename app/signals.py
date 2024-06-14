from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import RasterData
import os
from django.conf import settings


@receiver(pre_delete, sender=RasterData)
def delete_raster_data_files(sender, instance, **kwargs):
    # Delete the associated file from the media storage
    if instance.file_path:
        if os.path.isfile(instance.file_path):
            print(instance.file_path)
            os.remove(instance.file_path)

     # Delete the associated file from the media storage
    if instance.screenshot_image:
        if os.path.isfile(instance.screenshot_image.path):
            print(instance.screenshot_image.path)
            if not (instance.screenshot_image.path == f"{settings.BASE_DIR}/media/Uploads/RasterImage/raster_sample.png"):
                os.remove(instance.screenshot_image.path)

    # Delete the optimized files
    id_str = str(instance.id)
    # Replace with the actual path to the 'optimized' folder
    optimized_folder = f'{settings.BASE_DIR}/optimized/'
    optimized_filenames = [f'{id_str}_red.tif',
                           f'{id_str}_green.tif', f'{id_str}_blue.tif']

    for filename in optimized_filenames:
        file_path = os.path.join(optimized_folder, filename)
        if os.path.isfile(file_path):
            print(file_path, 'file path')
            os.remove(file_path)
        pass

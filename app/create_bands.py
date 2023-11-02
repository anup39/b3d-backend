import os
import math
import rasterio
import tempfile
from rasterio.enums import Resampling
from rasterio.io import  MemoryFile
from rasterio.shutil import copy
from  .models import RasterData


GDAL_CONFIG={'GDAL_TIFF_INTERNAL_MASK': True, 'GDAL_TIFF_OVR_BLOCKSIZE': 256, 'GDAL_CACHEMAX': 536870912, 'GDAL_SWATH_SIZE': 1073741824}
COG_PROFILE = {
    "count": 1,
    "driver": "GTiff",
    "interleave": "pixel",
    "tiled": True,
    "blockxsize": 256,
    "blockysize": 256,
    "photometric": "MINISBLACK",
    'nodata': 0.0,
    "ZLEVEL": 1,
    "ZSTD_LEVEL": 9,
    "BIGTIFF": "IF_SAFER",
}
IN_MEMORY_THRESHOLD = 10980 * 10980
RESAMPLING_METHODS = { "average": Resampling.average,
                       "nearest": Resampling.nearest,
                        "bilinear": Resampling.bilinear,
                        "cubic": Resampling.cubic,
                        }

def handleCreateBandsNormal(file_path , raster_id ,output_folder,model):
    try:
        print(f"*******Create Bands from single Tif ********")
        raster_data_instance = RasterData.objects.get(id=raster_id)
        raster_data_instance.status = "Processing Started"
        progress = 0
        raster_data_instance.progress = progress
        raster_data_instance.save()  
        with rasterio.Env(**GDAL_CONFIG):
            with rasterio.open(file_path) as src:
                for band_number, color in [(1, "red"), (2, "green"), (3, "blue")]:
                    raster_data_instance.status = f"Processing {color} Band"
                    #1
                    progress += 1
                    raster_data_instance.progress = progress
                    raster_data_instance.save()  
                    target_crs="epsg:3857"
                    resampling_method = "average"
                    compression = "ZSTD"
                    nproc = 1
                    reproject= False
                    in_memory= None
                    rs_method = RESAMPLING_METHODS[resampling_method]
                    if nproc == -1:
                        nproc = os.cpu_count() or 1  # Default to 1 if `cpu_count` returns None
                    output_file = f"{output_folder}/{raster_id}_{color}.tif"  # Adjust the naming as needed

                    profile = src.profile.copy()
                    profile.update(COG_PROFILE)

                    if in_memory is None:
                        in_memory = src.width * src.height < IN_MEMORY_THRESHOLD

                    if in_memory:
                        raster_data_instance.status = f"Processing {color} Band in Memory File"
                        #2
                        progress += 12
                        raster_data_instance.progress = progress
                        raster_data_instance.save()  
                        memfile = MemoryFile()
                        dst = memfile.open(**profile)
                    else:
                        raster_data_instance.status = f"Processing {color} Band in Temporary file due to Large File size"
                        #2
                        progress += 12
                        raster_data_instance.progress = progress
                        raster_data_instance.save()  
                        fileobj = tempfile.NamedTemporaryFile(dir=str(output_folder), suffix=".tif")
                        fileobj.close()
                        tempraster=fileobj.name
                        dst = rasterio.open(tempraster, "w", **profile)
                        
                    if reproject:
                        pass
                    else:
                        pass

                    windows = list(dst.block_windows(1))      

                    raster_data_instance.status = f"Processing {color} Band  for Masking"
                    #3
                    progress += 10
                    raster_data_instance.progress = progress
                    raster_data_instance.save()  
                    for _, w in windows:
                        block_data = src.read(window=w, indexes=[band_number])
                        dst.write(block_data, window=w)
                        block_mask = src.dataset_mask(window=w).astype("uint8")
                        dst.write_mask(block_mask, window=w)       
                    

                    # add overviews
                    if not in_memory:
                        # work around bug mapbox/rasterio#1497
                        dst.close()
                        dst = rasterio.open(tempraster, "r+")
                        pass
               

                    max_overview_level = math.ceil(
                        math.log2(
                            max(
                                dst.height // profile["blockysize"],
                                dst.width // profile["blockxsize"],
                                1,
                            )
                        )
                    )



                    if max_overview_level > 0:
                        overviews = [2**j for j in range(1, max_overview_level + 1)]
                        dst.build_overviews(overviews, rs_method)
                        dst.update_tags(ns="rio_overview", resampling=rs_method.value)


                    # copy to destination (this is necessary to push overviews to start of file)
                    copy(dst,str(output_file),copy_src_overviews=True,compress=compression,**COG_PROFILE,)   

                    if not in_memory:
                        os.remove(tempraster)
                        pass
                         

                    raster_data_instance.status = f"Processing {color} Band Completed"
                    #4
                    progress += 10
                    raster_data_instance.progress = progress
                    raster_data_instance.save()        


        raster_data_instance.status = f"Processing Completed"
        raster_data_instance.progress = 100
        raster_data_instance.is_display = True
        raster_data_instance.save() 
        return True

    except Exception as e:
        return str(e)
import os ,json
from .models import RasterData
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import exceptions
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rio_tiler.io import Reader
from rio_tiler.utils import non_alpha_indexes ,has_alpha_band
from rasterio.enums import ColorInterp
from rio_tiler.errors import TileOutsideBounds
from rio_tiler.profiles import img_profiles
import numpy as np
from django.utils.translation import gettext as _




ZOOM_EXTRA_LEVELS = 3


class TaskNestedView(APIView):
    queryset = RasterData.objects.all()
    # permission_classes = (AllowAny, )

    def get_and_check_raster(self, request, pk, annotate={}):
        try:
            raster = self.queryset.annotate(**annotate).get(pk=pk)
        except (ObjectDoesNotExist, ValidationError):
            raise exceptions.NotFound()

        return raster
    

class Metadata(TaskNestedView):
    def get(self, request, pk=None, project_pk=None, tile_type=""):
        """
        Get the metadata for this tasks's asset type
        """
        raster = self.get_and_check_raster(request, pk)
        raster_path = f"{settings.BASE_DIR}/media/"+str(raster.tif_file)
        if not os.path.isfile(raster_path):
            raise exceptions.NotFound()
   
        try:
            with Reader(raster_path) as src:
                # info = json.loads(metadata.json())
                info={}
                info['name'] = raster.name
                info['scheme'] = 'xyz'
                # if info['maxzoom'] < info['minzoom']:
                #     info['maxzoom'] = info['minzoom']
                # info['maxzoom'] += ZOOM_EXTRA_LEVELS
                # info['minzoom'] -= ZOOM_EXTRA_LEVELS
                info['bounds'] = {'value': src.bounds}
               
                # print(dir(src.dataset), 'bounds')
                return Response(info)
        except IndexError as e:
            # Caught when trying to get an invalid raster metadata
            raise exceptions.ValidationError("Cannot retrieve raster metadata: %s" % str(e))
        # # Override min/max

     
class Tiles(TaskNestedView):
    def get(self, request, pk=None, project_pk=None, tile_type="", z="", x="", y="", scale=1, ext=None):


        raster = self.get_and_check_raster(request, pk)

        z = int(z)
        x = int(x)
        y = int(y)

        scale = int(scale)
        rescale = None
        nodata = None
        indexes = None
        tilesize = 512
        expr =None


        raster_path = f"{settings.BASE_DIR}/media/"+str(raster.tif_file)
        
        if not os.path.isfile(raster_path):
            raise exceptions.NotFound()

        with Reader(raster_path) as src:
            if not src.tile_exists(x, y, z):
                raise exceptions.NotFound(_("Outside of bounds"))
            has_alpha = has_alpha_band(src.dataset)
            if tile_type == 'orthophoto' and expr is None:
                ci = src.dataset.colorinterp
                # More than 4 bands?
                if len(ci) > 4:
                    # Try to find RGBA band order
                    if ColorInterp.red in ci and \
                            ColorInterp.green in ci and \
                            ColorInterp.blue in ci:
                        indexes = (ci.index(ColorInterp.red) + 1,
                                   ci.index(ColorInterp.green) + 1,
                                   ci.index(ColorInterp.blue) + 1,)
                    else:

                        # Fallback to first three
                        indexes = (1, 2, 3,)

                elif has_alpha:
                    indexes = non_alpha_indexes(src.dataset)
           
            if nodata is None and tile_type == 'orthophoto':
                nodata = 0

            resampling = "nearest"
            padding = 0
            tile_buffer = None
            try:
                tile = src.tile(x, y, z, indexes=indexes, tilesize=tilesize, nodata=nodata,
                                padding=padding, 
                                resampling_method=resampling)
            except TileOutsideBounds:
                raise exceptions.NotFound(_("Outside of bounds"))

            # Auto?
            if ext is None:
                # Check for transparency
                if np.equal(tile.mask, 255).all():
                    ext = "jpg"
                else:
                    if 'image/webp' in request.headers.get('Accept', ''):
                        ext = "webp"
                    else:
                        ext = "png"

            driver = "jpeg" if ext == "jpg" else ext

            options = img_profiles.get(driver, {})

            rescale_arr = [17.0, 255.0]
          
            
            return HttpResponse(
                tile.post_process(in_range=(rescale_arr,)).render(img_format=driver, **options),
                content_type="image/{}".format(ext)
            )




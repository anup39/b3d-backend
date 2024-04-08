from rest_framework import routers
from .views import ExampleViewSet, CustomAuthToken, ClientViewSet, ProjectViewSet, ProjectPolygonGeoJSONAPIView
from .views import GlobalStandardCategoryViewSet, GlobalSubCategoryViewSet, GlobalCategoryViewSet, GlobalCategoryStyleViewSet
from .views import StandardCategoryViewSet, SubCategoryViewSet, CategoryViewSet, CategoryStyleViewSet
from .views import PolygonDataViewSet, LineStringDataViewSet, PointDataViewSet
from .views import RasterDataViewSet
from .views import MapMeasuringsViewSets
from .views import RoleViewSet, UserRoleViewSet, UserViewSet
from .views import PolygonDataGeoJSONAPIView, LineStringDataGeoJSONAPIView, PointDataGeoJSONAPIView, UploadGeoJSONAPIView, UploadCategoriesView, UploadCategoriesSaveView, MeasuringTableSummationView, DeleteUploadGeoJSONAPIView
from django.urls import path, include, re_path
from .views import StandardInspectionViewSet, SubInspectionViewSet, InspectionViewSet
from .views import InspectionReportViewSet, InspectionPhotoViewSet, InpsectionPhotoGeometryViewSet
from .views import CategoryBoundingBoxViewSet
# from .views import TaskStatusView
# from .tiler import Metadata, Tiles


router = routers.DefaultRouter()


router.register('users', UserViewSet)
router.register('global-roles', RoleViewSet)
router.register('global-standard-category', GlobalStandardCategoryViewSet)
router.register('global-sub-category', GlobalSubCategoryViewSet)
router.register('global-category', GlobalCategoryViewSet)
router.register('global-category-style', GlobalCategoryStyleViewSet)

router.register('clients', ClientViewSet)
router.register('projects', ProjectViewSet)
router.register('project-polygon', ProjectPolygonGeoJSONAPIView)
router.register('raster-data', RasterDataViewSet)

router.register('standard-category', StandardCategoryViewSet)
router.register('sub-category', SubCategoryViewSet)
router.register('category', CategoryViewSet)
router.register('category-style', CategoryStyleViewSet)

router.register('polygon-data', PolygonDataViewSet)
router.register('linestring-data', LineStringDataViewSet)
router.register('point-data', PointDataViewSet)

router.register('user-role', UserRoleViewSet)

router.register('standard-inspection', StandardInspectionViewSet)
router.register('sub-inspection', SubInspectionViewSet)
router.register('inspection', InspectionViewSet)

router.register('inspection-report', InspectionReportViewSet)
router.register('inspection-photo', InspectionPhotoViewSet)
router.register('inspection-photo-geometry', InpsectionPhotoGeometryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('example/', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('map-measurings/', MapMeasuringsViewSets.as_view()),
    path('category-point-geojson/',  PointDataGeoJSONAPIView.as_view(),
         name='category-point-geojson'),
    path('category-linestring-geojson/',  LineStringDataGeoJSONAPIView.as_view(),
         name='category-linestring-geojson'),
    path('category-polygon-geojson/',  PolygonDataGeoJSONAPIView.as_view(),
         name='category-polygon-geojson'),
    path('upload-geojson/', UploadGeoJSONAPIView.as_view(), name='upload_geojson'),
    path('delete-geojson/', DeleteUploadGeoJSONAPIView.as_view(),
         name='delete_geojson'),
    path('upload-categories/', UploadCategoriesView.as_view(),
         name='upload_categories'),
    path('save-upload/', UploadCategoriesSaveView.as_view(),
         name='save_upload'),
    path('measuring-table-summation/', MeasuringTableSummationView.as_view()),
    path('category-bounding-box/',  CategoryBoundingBoxViewSet.as_view()),
    #     path('project-polygon/', ProjectPolygonGeoJSONAPIView.as_view(),
    #          name='project-polygon'),
    # path('projects/<project_pk>/rasters/<pk>/<tile_type>/metadata/', Metadata.as_view(), name='metadata'),
    # path('projects/<project_pk>/rasters/<pk>/<tile_type>/tile/<z>/<x>/<y>/', Tiles.as_view() ,name="tile"),
]

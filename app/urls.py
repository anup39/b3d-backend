from rest_framework import routers
from .views import ExampleViewSet, CustomAuthToken, ClientViewSet, ProjectViewSet
from .views import GlobalStandardCategoryViewSet, GlobalSubCategoryViewSet, GlobalCategoryViewSet, GlobalCategoryStyleViewSet
from .views import StandardCategoryViewSet, SubCategoryViewSet, CategoryViewSet, CategoryStyleViewSet
from .views import PolygonDataViewSet
from .views import RasterDataViewSet
from .views import RoleViewSet, UserRoleViewSet, UserViewSet
from django.urls import path, include, re_path
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
router.register('raster-data', RasterDataViewSet)

router.register('standard-category', StandardCategoryViewSet)
router.register('sub-category', SubCategoryViewSet)
router.register('category', CategoryViewSet)
router.register('category-style', CategoryStyleViewSet)

router.register('polygon-data', PolygonDataViewSet)

router.register('user-role', UserRoleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('example/', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    # path('projects/<project_pk>/rasters/<pk>/<tile_type>/metadata/', Metadata.as_view(), name='metadata'),
    # path('projects/<project_pk>/rasters/<pk>/<tile_type>/tile/<z>/<x>/<y>/', Tiles.as_view() ,name="tile"),
]

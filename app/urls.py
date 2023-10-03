from rest_framework import routers
from .views import ExampleViewSet, CustomAuthToken, UserRegistrationView , ProjectViewSet
from .views import GlobalStandardCategoryViewSet, GlobalSubCategoryViewSet , GlobalCategoryViewSet ,GlobalCategoryStyleViewSet
from django.urls import path, include



router = routers.DefaultRouter()


router.register('projects',ProjectViewSet)
router.register(r'global-standard-category', GlobalStandardCategoryViewSet)
router.register(r'global-sub-category', GlobalSubCategoryViewSet)
router.register(r'global-category', GlobalCategoryViewSet)
router.register(r'global-category-style', GlobalCategoryStyleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('example/', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
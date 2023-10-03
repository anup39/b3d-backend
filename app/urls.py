from rest_framework import routers
from .views import ExampleViewSet, CustomAuthToken, UserRegistrationView , ProjectViewSet
from django.urls import path, include



router = routers.DefaultRouter()


router.register('projects',ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('example/', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
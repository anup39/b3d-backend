from rest_framework import routers
from .views import ExampleViewSet, CustomAuthToken
from django.urls import path, include



router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('app/example', ExampleViewSet.as_view({'get': 'list'}),
         name='example-api'),
    path('api-token-auth/', CustomAuthToken.as_view())
]
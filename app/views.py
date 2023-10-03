from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .tasks import handleExampleTask
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Project ,GlobalStandardCategory, GlobalSubCategory, GlobalCategory ,GlobalCategoryStyle
from .serializers import UserRegistrationSerializer , ProjectSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer


# Create your views here.


class ExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        # Your logic for processing the API request
        data = {
            'message': 'Hello, API!',
            'status': 'success'
        }
        # This is to be on to check the task and celery status
        # handleExampleTask.delay()

        return Response(data)
    

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    

# For standard Categories
class GlobalStandardCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalStandardCategorySerializer
    queryset = GlobalStandardCategory.objects.all()
    pagination_class = None

class GlobalSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalSubCategorySerializer
    queryset = GlobalSubCategory.objects.all()
    pagination_class = None

class GlobalCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalCategorySerializer
    queryset = GlobalCategory.objects.all()
    pagination_class = None

class GlobalCategoryStyleViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalCategoryStyleSerializer
    queryset = GlobalCategoryStyle.objects.all()
    pagination_class = None
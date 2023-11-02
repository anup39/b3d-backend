import os 
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from .tasks import handleExampleTask, handleCreateBandsNormal_
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics ,status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Project ,GlobalStandardCategory, GlobalSubCategory, GlobalCategory ,GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category ,CategoryStyle
from .models import PolygonData
from .models import RasterData
from .serializers import UserRegistrationSerializer , ProjectSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer
from .serializers import StandardCategorySerializer, SubCategorySerializer, CategorySerializer, CategoryStyleSerializer
from .serializers import PolygonDataSerializer
from .serializers import RasterDataSerializer
from .filters import ProjectFilter
from .filters import StandardCategoryFilter, SubCategoryFilter ,CategoryFilter ,CategoryStyleFilter
from .filters import GlobalSubCategoryFilter ,GlobalCategoryFilter
from .filters import RasterDataFilter
from .create_bands import handleCreateBandsNormal
from django.conf import settings
from celery.result import AsyncResult





# Create your views here.


class TaskStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        response_data = {
            'status': result.status,
            'result': result.result,
        }
        return Response(response_data)

class ExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        # Your logic for processing the API request
        data = {
            'message': 'Hello, API!',
            'status': 'success'
        }
        # This is to be on to check the task and celery status
        handleExampleTask.delay()

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
            'username': user.username
        })
    
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    

# For standard Categories
class GlobalStandardCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalStandardCategorySerializer
    queryset = GlobalStandardCategory.objects.all()
    pagination_class = None

class GlobalSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalSubCategorySerializer
    queryset = GlobalSubCategory.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalSubCategoryFilter
    pagination_class = None

class GlobalCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalCategorySerializer
    queryset = GlobalCategory.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalCategoryFilter
    pagination_class = None

class GlobalCategoryStyleViewSet(viewsets.ModelViewSet):
    serializer_class = GlobalCategoryStyleSerializer
    queryset = GlobalCategoryStyle.objects.all()
    pagination_class = None


#For project categories
class StandardCategoryViewSet(viewsets.ModelViewSet):

    queryset = StandardCategory.objects.filter(is_display=True)
    serializer_class = StandardCategorySerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandardCategoryFilter


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.filter(is_display=True)
    serializer_class = SubCategorySerializer 
    filter_backends = [DjangoFilterBackend,]
    filterset_class = SubCategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.filter(is_display=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryStyleViewSet(viewsets.ModelViewSet):

    queryset = CategoryStyle.objects.all()
    serializer_class = CategoryStyleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryStyleFilter


# For PolygonData
class PolygonDataViewSet(viewsets.ModelViewSet):
    queryset = PolygonData.objects.all()
    serializer_class = PolygonDataSerializer


# For RasterData
class RasterDataViewSet(viewsets.ModelViewSet):
    queryset = RasterData.objects.all()
    serializer_class = RasterDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RasterDataFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        id = serializer.data.get('id')
        file_path = os.path.join(settings.MEDIA_ROOT , serializer.data.get("path_of_file"))
        headers = self.get_success_headers(serializer.data)
        output_folder = os.path.join(settings.BASE_DIR ,"optimized")
        # result = handleCreateBandsNormal(file_path=file_path,raster_id=id,output_folder= output_folder) 

        result = handleCreateBandsNormal_.delay(file_path=file_path,raster_id=id,output_folder= output_folder ,model="RasterData") 
        task_id = result.task_id  

        # Update the RasterData instance with the task_id
        raster_data_instance = RasterData.objects.get(id=id)
        raster_data_instance.task_id = task_id
        raster_data_instance.save()  # Save the updated instance

        if result:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "Subprocess commands failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

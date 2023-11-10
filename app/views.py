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
from .models import Role, UserRole , UserProject
from .serializers import UserRegistrationSerializer , ProjectSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer
from .serializers import StandardCategorySerializer, SubCategorySerializer, CategorySerializer, CategoryStyleSerializer
from .serializers import PolygonDataSerializer
from .serializers import RasterDataSerializer
from .serializers import RoleSerializer, UserRoleSerializer, UserSerializer , UserProjectSerializer
from .filters import ProjectFilter
from .filters import StandardCategoryFilter, SubCategoryFilter ,CategoryFilter ,CategoryStyleFilter
from .filters import GlobalSubCategoryFilter ,GlobalCategoryFilter
from .filters import RasterDataFilter
from .filters import UserRoleFilter
from .filters import UserProjectFilter
from .create_bands import handleCreateBandsNormal
from django.conf import settings
from celery.result import AsyncResult
from .utils import handle_delete_request


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


#TODO When project created create the userproject also
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProjectSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProjectFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            user = request.user 
            if user is not None:
                role = UserRole.objects.get(user=user)
                if str(role) == "admin":
                    pass
                else:
                    user_projects = UserProject.objects.filter(user=user)
                    project_ids = user_projects.values_list('project_id', flat=True)  
                    queryset = queryset.filter(id__in=project_ids)
        except:
            # Continue with your existing code
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        payload = request.data
        if 'is_deleted' in payload:
            if payload.get('is_deleted') is True:
                result = handle_delete_request(id = kwargs.get('pk'), fk='project')
                if result:
                    return self.update(request, *args, **kwargs)
                return Response({'message': "Error in Deleting the project"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return self.update(request, *args, **kwargs)
    

# For standard Categories
class GlobalStandardCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalStandardCategory.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = GlobalStandardCategorySerializer
    pagination_class = None

class GlobalSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalSubCategory.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = GlobalSubCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalSubCategoryFilter
    pagination_class = None

class GlobalCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalCategory.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = GlobalCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalCategoryFilter
    pagination_class = None

class GlobalCategoryStyleViewSet(viewsets.ModelViewSet):
    queryset = GlobalCategoryStyle.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = GlobalCategoryStyleSerializer
    pagination_class = None


#For project categories
class StandardCategoryViewSet(viewsets.ModelViewSet):
    queryset = StandardCategory.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = StandardCategorySerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandardCategoryFilter


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = SubCategorySerializer 
    filter_backends = [DjangoFilterBackend,]
    filterset_class = SubCategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryStyleViewSet(viewsets.ModelViewSet):
    queryset = CategoryStyle.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = CategoryStyleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryStyleFilter


# For PolygonData
class PolygonDataViewSet(viewsets.ModelViewSet):
    queryset = PolygonData.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = PolygonDataSerializer


# For RasterData
class RasterDataViewSet(viewsets.ModelViewSet):
    queryset = RasterData.objects.filter(is_deleted=False).order_by('-created_at')
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


#For Roles 
class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = RoleSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = UserRoleSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = UserRoleFilter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= User.objects.filter(is_active=True)
    serializer_class = UserSerializer


class UserProjectViewSet(viewsets.ModelViewSet):
    queryset= UserProject.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = UserProjectSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = UserProjectFilter
    


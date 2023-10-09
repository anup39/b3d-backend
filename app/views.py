from rest_framework.response import Response
from rest_framework import viewsets
from .tasks import handleExampleTask
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
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
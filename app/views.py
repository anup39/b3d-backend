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
from .serializers import UserRegistrationSerializer , ProjectSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer
from .serializers import StandardCategorySerializer, SubCategorySerializer, CategorySerializer, CategoryStyleSerializer

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


#For project categories
class StandardCategoryViewSet(viewsets.ModelViewSet):

    queryset = StandardCategory.objects.filter(is_display=True)
    serializer_class = StandardCategorySerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['project',]
    # filter_class = StandardCategoryFilter


class SubCategoryViewSet(viewsets.ModelViewSet):

    queryset = SubCategory.objects.filter(is_display=True)
    serializer_class = SubCategorySerializer 
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['project','standard_category']
    # filter_class = SubCategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.filter(is_display=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['project','sub_category']
    # filter_class = CategoryFilter


class CategoryStyleViewSet(viewsets.ModelViewSet):

    queryset = CategoryStyle.objects.all()
    serializer_class = CategoryStyleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['project','category']
    # filter_class = CategoryStyleFilter
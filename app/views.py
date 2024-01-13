import os
import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from .tasks import handleExampleTask, handleCreateBandsNormal_
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Client, Project, GlobalStandardCategory, GlobalSubCategory, GlobalCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role, UserRole
from .serializers import ClientSerializer, ProjectSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer
from .serializers import StandardCategorySerializer, SubCategorySerializer, CategorySerializer, CategoryStyleSerializer
from .serializers import PolygonDataSerializer, LineStringDataSerializer, PointDataSerializer
from .serializers import RasterDataSerializer
from .serializers import RoleSerializer, UserRoleSerializer, UserSerializer
from .serializers import StandardCategoryControlSerializer
from .serializers import PolygonDataGeojsonSerializer, PointDataGeojsonSerializer, LineStringDataGeojsonSerializer, UploadGeoJSONSerializer
from .filters import ProjectFilter
from .filters import StandardCategoryFilter, SubCategoryFilter, CategoryFilter, CategoryStyleFilter
from .filters import GlobalSubCategoryFilter, GlobalCategoryFilter, GlobalCategoryStyleFilter
from .filters import RasterDataFilter
from .filters import UserRoleFilter
from django.contrib.gis.geos import (
    GEOSGeometry)
# from .create_bands import handleCreateBandsNormal
from django.conf import settings
# from celery.result import AsyncResult
from .utils import handle_delete_request
from django.db.models import Q
import geopandas as gpd
import json
import zipfile
from django.http import JsonResponse
import pandas as pd


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


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


# For Roles
class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = RoleSerializer


# For standard Categories
class GlobalStandardCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalStandardCategory.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = GlobalStandardCategorySerializer
    pagination_class = None


class GlobalSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalSubCategory.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = GlobalSubCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalSubCategoryFilter
    pagination_class = None


class GlobalCategoryViewSet(viewsets.ModelViewSet):
    queryset = GlobalCategory.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = GlobalCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalCategoryFilter
    pagination_class = None


class GlobalCategoryStyleViewSet(viewsets.ModelViewSet):
    queryset = GlobalCategoryStyle.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = GlobalCategoryStyleSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = GlobalCategoryStyleFilter
    pagination_class = None


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ClientSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     try:
    #         user = request.user
    #         if user is not None:
    #             role = UserRole.objects.get(user=user)
    #             if str(role) == "admin":
    #                 pass
    #             else:
    #                 # user_projects = UserProject.objects.filter(user=user)
    #                 project_ids = user_projects.values_list(
    #                     'project_id', flat=True)
    #                 queryset = queryset.filter(id__in=project_ids)
    #     except:
    #         # Continue with your existing code
    #         queryset = self.filter_queryset(queryset)

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('firstname')
        last_name = request.data.get('lastname')
        username_exist = User.objects.filter(Q(username=username)).exists()
        if username_exist:
            return Response({'message': "Username already exists"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        email_exist = User.objects.filter(Q(email=email)).exists()
        if email_exist:
            return Response({'message': "Email already exists"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        mutable_data = request.data.copy()
        mutable_data['name'] = first_name + " " + last_name
        mutable_data['user'] = user.id
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        payload = request.data
        if 'is_deleted' in payload:
            if payload.get('is_deleted') is True:
                result = handle_delete_request(
                    id=kwargs.get('pk'), fk='client')
                if result:
                    return self.update(request, *args, **kwargs)
                return Response({'message': "Error in Deleting the client"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return self.update(request, *args, **kwargs)


# TODO When project created create the userproject also
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        payload = request.data
        if 'is_deleted' in payload:
            if payload.get('is_deleted') is True:
                result = handle_delete_request(
                    id=kwargs.get('pk'), fk='project')
                if result:
                    return self.update(request, *args, **kwargs)
                return Response({'message': "Error in Deleting the project"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return self.update(request, *args, **kwargs)

# For RasterData


class RasterDataViewSet(viewsets.ModelViewSet):
    queryset = RasterData.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = RasterDataSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RasterDataFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        id = serializer.data.get('id')
        file_path = os.path.join(
            settings.MEDIA_ROOT, serializer.data.get("path_of_file"))
        headers = self.get_success_headers(serializer.data)
        output_folder = os.path.join(settings.BASE_DIR, "optimized")
        # result = handleCreateBandsNormal(file_path=file_path,raster_id=id,output_folder= output_folder)

        result = handleCreateBandsNormal_.delay(
            file_path=file_path, raster_id=id, output_folder=output_folder, model="RasterData")
        task_id = result.task_id

        # Update the RasterData instance with the task_id
        raster_data_instance = RasterData.objects.get(id=id)
        raster_data_instance.task_id = task_id
        # TODO : Check in local why the task id not saved to model

        raster_data_instance.save()  # Save the updated instance

        if result:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "Subprocess commands failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# For project categories
class StandardCategoryViewSet(viewsets.ModelViewSet):
    queryset = StandardCategory.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = StandardCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandardCategoryFilter


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = SubCategoryFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter


class CategoryStyleViewSet(viewsets.ModelViewSet):
    queryset = CategoryStyle.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = CategoryStyleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryStyleFilter


# For PolygonData

class PolygonDataViewSet(viewsets.ModelViewSet):
    queryset = PolygonData.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = PolygonDataSerializer


# For LineStringData
class LineStringDataViewSet(viewsets.ModelViewSet):
    queryset = LineStringData.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = LineStringDataSerializer

# For PointData


class PointDataViewSet(viewsets.ModelViewSet):
    queryset = PointData.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = PointDataSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = UserRoleSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = UserRoleFilter


class MapMeasuringsViewSets(APIView):
    def get(self, request, *args, **kwargs):

        if request.query_params:
            if request.query_params.get("client"):
                client_id = request.query_params.get("client")
                queryset = StandardCategory.objects.filter(client=client_id)
                serialized = StandardCategoryControlSerializer(
                    queryset, many=True)
                return Response(serialized.data)

            if request.query_params.get("project"):
                return Response({"message": request.query_params.get("project"), "section": "project"})

            if request.query_params.get("property"):
                return Response({"message": request.query_params.get("property"), "section": "property"})

        return Response({"messaage":  "No parameters found"})


# Geojson for the agriplot
class PolygonDataGeoJSONAPIView(generics.ListAPIView):
    serializer_class = PolygonDataGeojsonSerializer

    def get_queryset(self):
        project = self.request.query_params.get('project', None)
        category = self.request.query_params.get('category', None)

        queryset = PolygonData.objects.filter(is_display=True)
        if project:
            queryset = queryset.filter(project=project)
        if category:
            queryset = queryset.filter(category=category)

        return queryset

# Geojson for the agriplot


class PointDataGeoJSONAPIView(generics.ListAPIView):
    serializer_class = PointDataGeojsonSerializer

    def get_queryset(self):
        project = self.request.query_params.get('project', None)
        category = self.request.query_params.get('category', None)

        queryset = PointData.objects.filter(is_display=True)
        if project:
            queryset = queryset.filter(project=project)
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class LineStringDataGeoJSONAPIView(generics.ListAPIView):
    serializer_class = LineStringDataGeojsonSerializer

    def get_queryset(self):
        project = self.request.query_params.get('project', None)
        category = self.request.query_params.get('category', None)

        queryset = LineStringData.objects.filter(is_display=True)
        if project:
            queryset = queryset.filter(project=project)
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class UploadGeoJSONAPIView(APIView):
    def post(self, request):
        file = request.data.get('file')
        type_of_file = request.data.get('type_of_file')
        filename = str(uuid.uuid4()) + '_' + file.name
        try:
            destination_path = f"media/Uploads/UploadVector/{filename}"
            with open(destination_path, 'wb') as destination_file:
                for chunk in file.chunks():
                    destination_file.write(chunk)
        except Exception as e:
            return JsonResponse({'message': 'Error saving file'}, status=500)

        # Create a directory to extract the contents of the zip file
        if type_of_file == "Shapefile":
            ZIP_FILE_PATH = destination_path
            filename_no_ext = ZIP_FILE_PATH.split("/")[-1].split(".")[0]
            EXTRACTED_PATH = f"media/Uploads/UploadVector/{filename_no_ext}/"
            os.makedirs(EXTRACTED_PATH, exist_ok=True)
            with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(EXTRACTED_PATH)
            extracted_files = os.listdir(EXTRACTED_PATH)
            folder_paths = [f for f in extracted_files if os.path.isdir(
                os.path.join(EXTRACTED_PATH, f))]

            if not folder_paths:
                return JsonResponse({'message': 'No layers found.'})

            SHAPEFILE_PATHS = []

            for folder_path in folder_paths:
                # Check if .shp file exists in the folder
                shp_file_path = os.path.join(
                    EXTRACTED_PATH, folder_path, f"{folder_path}.shp")
                if os.path.isfile(shp_file_path):
                    SHAPEFILE_PATHS.append(shp_file_path)

            if not SHAPEFILE_PATHS:
                # No .shp files found in the folders
                return JsonResponse({'message': 'No .shp files found.'})

            geojson_layers = []
            layers = []

            for shapefile_path in SHAPEFILE_PATHS:
                gdf = gpd.read_file(shapefile_path)
                geojson_data = gdf.to_crs(epsg='4326').to_json()
                layer_name = shapefile_path.split("/")[-1].split(".")[0]
                geojson_dict = json.loads(geojson_data)
                bounding_box_4326 = gdf.to_crs(epsg='4326').total_bounds
                geojson_layers.append(
                    {"layername": layer_name, "extent": [
                        bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]], "geojson": geojson_dict})
                layers.append({"layername": layer_name, "extent": [
                    bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]]})

            return Response({"file": filename, 'layers': layers,  "result": geojson_layers})
        else:
            GEOJSON_PATH = destination_path
            if not GEOJSON_PATH:
                return JsonResponse({'message': 'No layers found.'})
            geojson_layers = []
            layers = []
            gdf = gpd.read_file(GEOJSON_PATH)
            geojson_data = gdf.to_crs(epsg='4326').to_json()
            layer_name = GEOJSON_PATH.split("/")[-1].split(".")[0]
            filename_parts = layer_name.split('_')
            layer_name = filename_parts[1]
            geojson_dict = json.loads(geojson_data)
            bounding_box_4326 = gdf.to_crs(epsg='4326').total_bounds
            geojson_layers.append(
                {"layername": layer_name, "extent": [
                    bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]], "geojson": geojson_dict})
            layers.append({"layername": layer_name, "extent": [
                bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]]})
            return Response({"file": filename, 'layers': layers,  "result": geojson_layers})


class UploadCategoriesView(APIView):

    def get(self, request):
        type_of_file = self.request.query_params.get('type_of_file', None)
        filename = self.request.query_params.get('filename', None)
        destination_path = f"media/Uploads/UploadVector/{filename}"

        if type_of_file == "Geojson":
            GEOJSON_PATH = destination_path
            if not os.path.isfile(GEOJSON_PATH):
                return Response({'message': 'No layers found.'})

            gdf = gpd.read_file(GEOJSON_PATH)
            distinct_values = gdf['name'].unique()
            # find the type of geometry for each of the distinct values
            distinct_values_list = []
            layers = []
            id = 1
            for value in distinct_values:
                distinct_values_dict = {}
                distinct_values_dict['filename'] = filename
                distinct_values_dict['id'] = id
                distinct_values_dict['name'] = value
                distinct_values_dict['type_of_geometry'] = gdf[gdf['name']
                                                               == value].geometry.iloc[0].geom_type
                distinct_values_dict['matched_category'] = None
                distinct_values_dict['checked'] = False

                distinct_values_list.append(distinct_values_dict)
                id += 1

            return Response({'type of file': type_of_file, "distinct": distinct_values_list})
        else:
            ZIP_FILE_PATH = destination_path
            filename_no_ext = ZIP_FILE_PATH.split(
                "/")[-1].split(".")[0]
            EXTRACTED_PATH = f"media/Uploads/UploadVector/{filename_no_ext}/"
            extracted_files = os.listdir(EXTRACTED_PATH)
            folder_paths = [f for f in extracted_files if os.path.isdir(
                os.path.join(EXTRACTED_PATH, f))]

            if not folder_paths:
                return Response({'message': 'No layers found.'})

            SHAPEFILE_PATHS = []

            for folder_path in folder_paths:
                # Check if .shp file exists in the folder
                shp_file_path = os.path.join(
                    EXTRACTED_PATH, folder_path, f"{folder_path}.shp")
                if os.path.isfile(shp_file_path):
                    SHAPEFILE_PATHS.append(shp_file_path)

            if not SHAPEFILE_PATHS:
                # No .shp files found in the folders
                return Response({'message': 'No .shp files found.'})

            layers = []
            for shapefile_path in SHAPEFILE_PATHS:
                gdf = gpd.read_file(shapefile_path)
                # geojson_data = gdf.to_crs(epsg='4326').to_json()
                layer_name = shapefile_path.split("/")[-1].split(".")[0]
                distinct_values = gdf['undertype'].unique()
                # distinct_values_list = []
                id = 1
                for value in distinct_values:
                    distinct_values_dict = {}
                    distinct_values_dict['filename'] = filename
                    distinct_values_dict['id'] = id
                    distinct_values_dict['layername'] = layer_name
                    distinct_values_dict['name'] = value
                    distinct_values_dict['type_of_geometry'] = gdf[gdf['undertype']
                                                                   == value].geometry.iloc[0].geom_type
                    distinct_values_dict['matched_category'] = None
                    distinct_values_dict['checked'] = False
                    id += 1

                    # distinct_values_list.append(distinct_values_dict)
                    layers.append(distinct_values_dict)

            return Response({'type of file': type_of_file, "distinct": layers})


def checkUploadFileValidationGlobal(shape_file):

    if not shape_file.name.endswith('.zip'):
        raise ValidationError('The file must be a ZIP archive.')
    if shape_file.name.endswith('.zip'):
        # Open the zip file
        with zipfile.ZipFile(shape_file, 'r') as zip_file:

            # Check if a file with a .shp extension exists in the zip file
            file_list = zip_file.namelist()
            shp_file = None
            for file_name in file_list:
                if file_name.endswith('.shp'):
                    shp_file = file_name
                    break

            # If a .shp file exists, open it
            if shp_file:
                with zip_file.open(shp_file) as file:
                    pass
            else:
                raise ValueError(
                    f"No .shp file found in {shape_file}")


def handleDataframeSave(client_id, user_id, project_id, dataframe):
    # print("herer in upload")
    gdf = dataframe
    gdf = gdf.to_crs(epsg=4326)
    user = User.objects.get(id=user_id)
    client = Client.objects.get(id=client_id)
    project = Project.objects.get(id=project_id)
    for index, row in gdf.iterrows():
        geom = GEOSGeometry(str(row["geometry"]))
        matched_category = row['matched_category']

        category = Category.objects.get(id=matched_category)

        if geom.geom_type == "MultiPolygon" and category.type_of_geometry == "Polygon":
            for polygon in geom:
                PolygonData.objects.create(
                    client=client,
                    project=project,
                    standard_category=category.standard_category,
                    sub_category=category.sub_category,
                    category=category,
                    standard_category_name=category.standard_category.name,
                    sub_category_name=category.sub_category.name,
                    category_name=category.name,
                    geom=polygon,
                    created_by=user
                )
        elif geom.geom_type == "Polygon" and category.type_of_geometry == "Polygon":
            PolygonData.objects.create(
                client=client,
                project=project,
                standard_category=category.standard_category,
                sub_category=category.sub_category,
                category=category,
                standard_category_name=category.standard_category.name,
                sub_category_name=category.sub_category.name,
                category_name=category.name,
                geom=geom,
                created_by=user
            )

        elif geom.geom_type == "MultiLineString" and category.type_of_geometry == "LineString":
            for line in geom:
                LineStringData.objects.create(
                    client=client,
                    project=project,
                    standard_category=category.standard_category,
                    sub_category=category.sub_category,
                    category=category,
                    standard_category_name=category.standard_category.name,
                    sub_category_name=category.sub_category.name,
                    category_name=category.name,
                    geom=line,
                    created_by=user
                )
        elif geom.geom_type == "LineString" and category.type_of_geometry == "LineString":
            LineStringData.objects.create(
                client=client,
                project=project,
                standard_category=category.standard_category,
                sub_category=category.sub_category,
                category=category,
                standard_category_name=category.standard_category.name,
                sub_category_name=category.sub_category.name,
                category_name=category.name,
                geom=geom,
                created_by=user
            )
        elif geom.geom_type == "MultiPoint" and category.type_of_geometry == "Point":
            for point in geom:
                PointData.objects.create(
                    client=client,
                    project=project,
                    standard_category=category.standard_category,
                    sub_category=category.sub_category,
                    category=category,
                    standard_category_name=category.standard_category.name,
                    sub_category_name=category.sub_category.name,
                    category_name=category.name,
                    geom=point,
                    created_by=user
                )
        elif geom.geom_type == "Point" and category.type_of_geometry == "Point":
            PointData.objects.create(
                client=client,
                project=project,
                standard_category=category.standard_category,
                sub_category=category.sub_category,
                category=category,
                standard_category_name=category.standard_category.name,
                sub_category_name=category.sub_category.name,
                category_name=category.name,
                geom=geom,
                created_by=user
            )

    return True


class UploadCategoriesSaveView(APIView):
    # for shapefile[
    #     {
    #         "filename": "bd604947-ef4f-451f-8c68-e5078b379fc1_export.zip",
    #         "id": 1,
    #         "layername": "Udstyr punkt",
    #         "name": "Afløbsrist",
    #         "type_of_geometry": "Point",
    #         "matched_category": 27,
    #         "checked": true
    #     }
    # ]

    def post(self, request):
        type_of_file = request.data.get('type_of_file')
        filename = request.data.get('filename')
        destination_path = f"media/Uploads/UploadVector/{filename}"

        if type_of_file == "Geojson":
            GEOJSON_PATH = destination_path
            if not os.path.isfile(GEOJSON_PATH):
                return Response({'message': 'No layers found.'})
            result = request.data.get('result')
            result = json.loads(result)
            gdf = gpd.read_file(GEOJSON_PATH)
            gdf.to_crs(epsg='4326')
            names = [i['name'] for i in result]
            # print(names, 'names')
            filtered_gdf = gdf[gdf['name'].isin(names)]
            filtered_gdf['matched_category'] = filtered_gdf['name'].map(
                lambda x: next((item for item in result if item["name"] == x), None)['matched_category'])

            handleDataframeSave(client_id=request.data.get('client_id'), user_id=request.data.get(
                'user_id'), project_id=request.data.get('project_id'), dataframe=filtered_gdf)

            return Response({'message': "Sucessfully saved the data"})
        else:
            ZIP_FILE_PATH = destination_path
            filename_no_ext = ZIP_FILE_PATH.split(
                "/")[-1].split(".")[0]
            EXTRACTED_PATH = f"media/Uploads/UploadVector/{filename_no_ext}/"
            extracted_files = os.listdir(EXTRACTED_PATH)
            folder_paths = [f for f in extracted_files if os.path.isdir(
                os.path.join(EXTRACTED_PATH, f))]

            if not folder_paths:
                return Response({'message': 'No layers found.'})

            SHAPEFILE_PATHS = []

            for folder_path in folder_paths:
                # Check if .shp file exists in the folder
                shp_file_path = os.path.join(
                    EXTRACTED_PATH, folder_path, f"{folder_path}.shp")
                if os.path.isfile(shp_file_path):
                    SHAPEFILE_PATHS.append(shp_file_path)

            if not SHAPEFILE_PATHS:
                # No .shp files found in the folders
                return Response({'message': 'No .shp files found.'})

            layers = []
            result = request.data.get('result')
            result = json.loads(result)
            new_list = []
            layer_names = set(item['layername'] for item in result)

            for layer_name in layer_names:
                filtered_items = [
                    item for item in result if item['layername'] == layer_name]
                new_list.append(filtered_items)

            # print(new_list, 'new_list')
            for shapefile_path in SHAPEFILE_PATHS:
                # print(shapefile_path, 'shapefile_path')
                for result_ in new_list:
                    layer_name = shapefile_path.split("/")[-1].split(".")[0]
                    if (result_[0].get('layername') == layer_name):
                        gdf = gpd.read_file(shapefile_path)
                        gdf.to_crs(epsg='4326')
                        names = [i['name'] for i in result_]
                        # print(names, 'names')
                        filtered_gdf = gdf[gdf['undertype'].isin(names)]
                        filtered_gdf['matched_category'] = filtered_gdf['undertype'].map(
                            lambda x: next((item for item in result_ if item["name"] == x), None)['matched_category'])

                        handleDataframeSave(client_id=request.data.get('client_id'), user_id=request.data.get(
                            'user_id'), project_id=request.data.get('project_id'), dataframe=filtered_gdf)

            return Response({'message': "Sucessfully saved the data"})


class MeasuringTableSummationView(APIView):
    def get(self, request):
        project_id = request.query_params.get('project_id')
        client_id = request.query_params.get('client_id')

        return Response({'message': "Sccess", 'project_id': project_id, 'client_id': client_id})

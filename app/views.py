import os
import uuid
from rest_framework.response import Response
from rest_framework import viewsets
from .tasks import handleExampleTask, handleCreateBandsNormal_
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.models import User
from .models import Client, Project, GlobalStandardCategory, GlobalSubCategory, GlobalCategory, GlobalCategoryStyle, ProjectPolygon
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role, UserRole
from .serializers import ClientSerializer, ProjectSerializer, ProjectPolygonGeojsonSerializer
from .serializers import GlobalStandardCategorySerializer, GlobalSubCategorySerializer, GlobalCategorySerializer, GlobalCategoryStyleSerializer
from .serializers import StandardCategorySerializer, SubCategorySerializer, CategorySerializer, CategoryStyleSerializer
from .serializers import PolygonDataSerializer, LineStringDataSerializer, PointDataSerializer
from .serializers import RasterDataSerializer
from .serializers import RoleSerializer, UserRoleSerializer, UserSerializer
from .serializers import StandardCategoryControlSerializer
from .serializers import PolygonDataGeojsonSerializer, PointDataGeojsonSerializer, LineStringDataGeojsonSerializer, UploadGeoJSONSerializer
from .filters import ProjectFilter, ProjectPolygonFilter
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
import numpy as np
import django_filters

from .serializers import StandardInspectionSerializer, SubInspectionSerializer, InspectionSerializer
from .models import StandardInspection, SubInspection, Inspection
from .serializers import InspectionReportSerializer, InspectionPhotoSerializer, InpsectionPhotoGeometrySerializer
from .models import InspectionReport, InspectionPhoto, InpsectionPhotoGeometry
from django.contrib.gis.db.models.functions import Area
from django.contrib.gis.db.models import Sum, Transform
from django.db.models import FloatField, ExpressionWrapper
from shapely import wkt
from fuzzywuzzy import process
import re
import math
import time


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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProjectFilter
    search_fields = ['name', 'description']

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


class ProjectPolygonGeoJSONAPIView(viewsets.ModelViewSet):
    serializer_class = ProjectPolygonGeojsonSerializer
    queryset = ProjectPolygon.objects.filter(is_display=True)
    filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ['project', 'client']
    filterset_class = ProjectPolygonFilter


# For RasterData
class RasterDataViewSet(viewsets.ModelViewSet):
    queryset = RasterData.objects.filter(
        is_deleted=False).order_by('created_at')
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
        client = self.request.query_params.get('client', None)
        project = self.request.query_params.get('project', None)
        category = self.request.query_params.get('category', None)

        queryset = PolygonData.objects.filter(is_display=True)
        if client:
            print(client, 'client')
            queryset = queryset.filter(client=client)
        if project:
            print(project, 'project')
            queryset = queryset.filter(project=project)
        if category:
            print(category, 'category')
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


def delete_geojson_file(filename):
    destination_path = f"media/Uploads/UploadVector/{filename}"
    try:
        standard_path = f"media/Uploads/UploadVector/{filename}_standardized.geojson"
        exploded_path = f"media/Uploads/UploadVector/{filename}_exploded.geojson"
        if os.path.isfile(standard_path):
            os.remove(standard_path)
        if os.path.isfile(exploded_path):
            os.remove(exploded_path)
    except:
        pass
    if os.path.isfile(destination_path):
        os.remove(destination_path)
        return True
    return False


class UploadGeoJSONAPIView(APIView):
    def post(self, request):
        import time
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
            try:
                start_time = time.time()
                gdf = gpd.read_file(GEOJSON_PATH)
                gdf = gdf.apply(lambda col: col.astype(
                    str) if col.dtype == 'datetime64[ns]' else col)
                end_time = time.time()
                execution_time = end_time - start_time
                print(
                    f'Time taken to execute the code: {execution_time} seconds')
            except Exception as e:
                delete_geojson_file(filename)
                return JsonResponse({'message': f'Error reading the file. {str(e)}'}, status=500)
            geojson_data = gdf.to_crs(epsg='4326').to_json()
            layer_name = GEOJSON_PATH.split("/")[-1].split(".")[0]
            filename_parts = layer_name.split('_')
            layer_name = filename_parts[1] if len(
                filename_parts) > 1 else layer_name
            geojson_dict = json.loads(geojson_data)
            bounding_box_4326 = gdf.to_crs(epsg='4326').total_bounds
            geojson_layers.append(
                {"layername": layer_name, "extent": [
                    bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]], "geojson": geojson_dict})
            layers.append({"layername": layer_name, "extent": [
                bounding_box_4326[0], bounding_box_4326[1], bounding_box_4326[2], bounding_box_4326[3]]})
            return Response({"file": filename, 'layers': layers,  "result": geojson_layers})


class DeleteUploadGeoJSONAPIView(APIView):
    def post(self, request):
        filename = request.data.get('filename')
        deleted = delete_geojson_file(filename)
        if (deleted):
            return JsonResponse({'message': 'File deleted successfully.'})
        return JsonResponse({'message': 'File not found.'}, status=404)

# Cleaning and matiching data


def clean_text(text):
    text = text.lower()
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.strip()
    return text


def clean_name(name, unique_cleaned_distinct_values, component):
    name = re.sub(r'\d+', '', name.lower()).strip()
    best_match, score = process.extractOne(
        name, unique_cleaned_distinct_values)
    return best_match if score >= 90 else (name if component == "clean" else None)


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
            column_name = 'name' if 'name' in gdf.columns else 'undertype'
            distinct_values = gdf[column_name]

            unique_cleaned_distinct_values = distinct_values.apply(
                clean_text).unique()
            print(unique_cleaned_distinct_values,
                  "unique_cleaned_distinct_values")
            print("************Starting Cleaning************")
            unique_values = distinct_values.unique()
            cleaned_names = {name: clean_name(
                name, unique_cleaned_distinct_values, "clean") for name in unique_values}
            gdf['cleaned_name'] = distinct_values.map(cleaned_names)
            print("************Completed cleaning ************")

            categories_polygon = dict(Category.objects.filter(
                client_id=request.query_params.get('client_id', None), type_of_geometry="Polygon").values_list('name', 'id'))
            categories_linestring = dict(Category.objects.filter(
                client_id=request.query_params.get('client_id', None), type_of_geometry="LineString").values_list('name', 'id'))
            categories_point = dict(Category.objects.filter(
                client_id=request.query_params.get('client_id', None), type_of_geometry="Point").values_list('name', 'id'))

            print(categories_polygon, 'categories_polygon')
            print(categories_linestring, 'categories_linestring')
            print(categories_point, 'categories_point')

            def match_category(name, geometry):
                geometry = geometry.type
                if geometry == "Polygon" or geometry == "MultiPolygon":
                    match = process.extractOne(
                        name.lower().strip(), categories_polygon.keys())
                    if match is None:
                        return None
                    best_match, score = match
                    return categories_polygon[best_match] if score >= 90 else None
                elif geometry == "LineString" or geometry == "MultiLineString":
                    match = process.extractOne(
                        name.lower().strip(), categories_linestring.keys())
                    if match is None:
                        return None
                    best_match, score = match
                    return categories_linestring[best_match] if score >= 90 else None
                else:
                    match = process.extractOne(
                        name.lower().strip(), categories_point.keys())
                    if match is None:
                        return None
                    best_match, score = match
                    return categories_point[best_match] if score >= 90 else None

            gdf['matched_category'] = gdf.apply(lambda row: match_category(
                row['cleaned_name'], row['geometry']), axis=1)
            gdf['matched_category'] = gdf['matched_category'].astype('Int64')

            distinct_values_final = []

            gdf_polygon = gdf.loc[gdf.geometry.type.isin(
                ["MultiPolygon", "Polygon"])]
            print(len(gdf), 'length of multipolygon or polygon')
            gdf_polygon = gdf_polygon.drop_duplicates(subset='cleaned_name')
            distinct_values_final.append(
                gdf_polygon[[
                    'cleaned_name', 'matched_category']].to_dict('records')
            )

            gdf_linestring = gdf.loc[gdf.geometry.type.isin(
                ["MultiLineString", "LineString"])]
            print(len(gdf_linestring), 'length of multiline or linestring')
            gdf_linestring = gdf_linestring.drop_duplicates(
                subset='cleaned_name')
            distinct_values_final.append(
                gdf_linestring[[
                    'cleaned_name', 'matched_category']].to_dict('records')
            )

            gdf_point = gdf.loc[gdf.geometry.type.isin(
                ["MultiPoint", "Point"])]
            print(len(gdf_point), 'length of multipolygon or polygon')
            gdf_point = gdf_point.drop_duplicates(subset='cleaned_name')
            distinct_values_final.append(
                gdf_point[[
                    'cleaned_name', 'matched_category']].to_dict('records')
            )

            # Iterate over all columns in the GeoDataFrame
            for col in gdf.columns:
                # If the column data type is 'Timestamp', convert it to string
                if gdf[col].dtype == 'datetime64[ns]':
                    gdf[col] = gdf[col].astype(str)

            # Now you can write to a JSON file
            with open(f'{destination_path}_standardized.geojson', 'w') as f:
                f.write(gdf.to_json())

            print(distinct_values_final, 'distinct_values_final')

            print("************Completed Matching ************")
            return Response({'type_of_file': type_of_file, "distinct": distinct_values_final})

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

            return Response({'type_of_file': type_of_file, "distinct": layers})


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


def handleDataframeSave(client_id, user_id, project_id, dataframe, result):
    # print("herer in upload")
    gdf = dataframe
    user = User.objects.get(id=user_id)
    client = Client.objects.get(id=client_id)
    project = Project.objects.get(id=project_id)
    for index, row in gdf.iterrows():
        geom = GEOSGeometry(str(row["geometry"]))
        cleaned_name = row['cleaned_name']
        category_ids = [item['category_id']
                        for item in result if item['cleaned_name'] == cleaned_name]
        print(category_ids)
        # category_id = row['category_id']

        category = Category.objects.get(id=category_ids[0])

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
    def post(self, request):
        type_of_file = request.data.get('type_of_file')
        filename = request.data.get('filename')
        destination_path = f"media/Uploads/UploadVector/{filename}_standardized.geojson"
        print(destination_path, 'destination_path')

        df = None
        gdf_polygon = None
        gdf_linestring = None
        gdf_point = None

        if type_of_file == "Geojson":
            GEOJSON_PATH = destination_path
            if not os.path.isfile(GEOJSON_PATH):
                return Response({'message': 'No layers found.'})
            result = request.data.get('result')
            result = json.loads(result)
            filtered_result = []
            for item in result:
                inner_result = []
                for i in item:
                    if i.get('checked') and i.get('matched_category'):
                        inner_result.append(i)
                filtered_result.append(inner_result)
            print(filtered_result, 'filtered_result')

            df = gpd.read_file(GEOJSON_PATH)
            df.to_crs(epsg='4326', inplace=True)

            print(df, 'dataframe')

            client = Client.objects.get(id=request.data.get('client_id'))
            project = Project.objects.get(id=request.data.get('project_id'))
            user = User.objects.get(id=request.data.get('user_id'))
            categories = {
                category.id: category for category in Category.objects.all()}
            standard_categories = {
                standard_category.id: standard_category for standard_category in StandardCategory.objects.all()}
            sub_categories = {
                sub_category.id: sub_category for sub_category in SubCategory.objects.all()}

            # For Polygon
            names_to_filter_polygon = []
            for item in filtered_result[0]:
                print(item, 'item ')
                names_to_filter_polygon.append(
                    item.get('cleaned_name'))
            print(names_to_filter_polygon, 'names_to_filter_polygon')
            gdf_polygon = df[df['cleaned_name'].isin(names_to_filter_polygon)]
            print(gdf_polygon, 'gdf_polygon')
            gdf_polygon = gdf_polygon.copy()  # Create a copy to avoid SettingWithCopyWarning
            gdf_polygon.loc[:, 'project'] = request.data.get('project_id')
            gdf_polygon.loc[:, 'client'] = request.data.get('client_id')
            gdf_polygon.loc[:, 'client'] = gdf_polygon['client'].astype(
                'Int64')
            gdf_polygon.loc[:, 'project'] = gdf_polygon['project'].astype(
                'Int64')
            gdf_polygon = gdf_polygon.loc[gdf_polygon.geometry.type.isin(
                ["MultiPolygon", "Polygon"])]

            def create_category_polygon(name):
                for i in filtered_result[0]:
                    if i.get('cleaned_name') == name:
                        return i.get('matched_category')

            gdf_polygon.loc[:, 'category'] = gdf_polygon.apply(lambda row: create_category_polygon(
                row['cleaned_name']), axis=1)
            gdf_polygon.loc[:, 'category'] = gdf_polygon['category'].astype(
                'Int64')
            gdf_polygon.loc[:, 'standard_category'] = gdf_polygon['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.id)
            gdf_polygon.loc[:, 'standard_category'] = gdf_polygon['standard_category'].astype(
                'Int64')
            gdf_polygon.loc[:, 'sub_category'] = gdf_polygon['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.id)
            gdf_polygon.loc[:, 'sub_category'] = gdf_polygon['sub_category'].astype(
                'Int64')
            gdf_polygon.loc[:, 'standard_category_name'] = gdf_polygon['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.name)
            gdf_polygon.loc[:, 'sub_category_name'] = gdf_polygon['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.name)
            gdf_polygon.loc[:, 'category_name'] = gdf_polygon['category'].map(
                lambda x: Category.objects.get(id=x).name)
            gdf_polygon.loc[:, 'created_by'] = request.data.get('user_id')
            gdf_polygon.loc[:, 'is_display'] = True

            print(gdf_polygon[[
                  'project', 'client', 'standard_category', 'sub_category', 'category', 'standard_category_name', 'sub_category_name', 'category_name', 'created_by', 'is_display']].head(15))
            print(len(gdf_polygon), 'length of gdf_polygon')
            gdf_polygon = gdf_polygon.explode(ignore_index=True)
            print(len(gdf_polygon), 'length of gdf_polygon after explode')

            start_time = time.time()
            polygon_data_list = [
                PolygonData(
                    client=client,
                    project=project,
                    standard_category=standard_categories[row['standard_category']],
                    sub_category=sub_categories[row['sub_category']],
                    category=categories[row['category']],
                    standard_category_name=standard_categories[row['standard_category']].name,
                    sub_category_name=sub_categories[row['sub_category']].name,
                    category_name=categories[row['category']].name,
                    geom=GEOSGeometry(row['geometry'].wkt),
                    created_by=user,
                    is_display=row['is_display'],
                )
                for _, row in gdf_polygon.iterrows()
            ]

            PolygonData.objects.bulk_create(polygon_data_list)
            end_time = time.time()
            execution_time = end_time - start_time
            print(
                f'Time taken to upload Polygon {len(gdf_polygon)} the code: {execution_time} seconds')

            # For LinesTring
            names_to_filter_linestring = []
            for item in filtered_result[1]:
                names_to_filter_linestring.append(
                    item.get('cleaned_name'))

            gdf_linestring = df[df['cleaned_name'].isin(
                names_to_filter_linestring)]
            gdf_linestring = gdf_linestring.copy()
            gdf_linestring['project'] = request.data.get('project_id')
            gdf_linestring['client'] = request.data.get('client_id')
            gdf_linestring['client'] = gdf_linestring['client'].astype('Int64')
            gdf_linestring['project'] = gdf_linestring['project'].astype(
                'Int64')
            gdf_linestring = gdf_linestring.loc[gdf_linestring.geometry.type.isin(
                ["MultiLineString", "LineString"])]

            def create_category_linestring(name):
                for i in filtered_result[1]:
                    if i.get('cleaned_name') == name:
                        return i.get('matched_category')
            gdf_linestring['category'] = gdf_linestring.apply(lambda row: create_category_linestring(
                row['cleaned_name']), axis=1)
            gdf_linestring['category'] = gdf_linestring['category'].astype(
                'Int64')
            gdf_linestring['standard_category'] = gdf_linestring['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.id)
            gdf_linestring['standard_category'] = gdf_linestring['standard_category'].astype(
                'Int64')
            gdf_linestring['sub_category'] = gdf_linestring['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.id)
            gdf_linestring['sub_category'] = gdf_linestring['sub_category'].astype(
                'Int64')
            gdf_linestring['standard_category_name'] = gdf_linestring['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.name)
            gdf_linestring['sub_category_name'] = gdf_linestring['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.name)
            gdf_linestring['category_name'] = gdf_linestring['category'].map(
                lambda x: Category.objects.get(id=x).name)
            gdf_linestring['created_by'] = request.data.get('user_id')
            gdf_linestring['is_display'] = True

            print(gdf_linestring[[
                'project', 'client', 'standard_category', 'sub_category', 'category', 'standard_category_name', 'sub_category_name', 'category_name', 'created_by', 'is_display']].head(15))
            print(len(gdf_linestring), 'length of gdf_linestring')
            gdf_linestring = gdf_linestring.explode(ignore_index=True)
            print(len(gdf_linestring), 'length of gdf_linestring after explode')

            start_time = time.time()
            linestring_data_list = [
                LineStringData(
                    client=client,
                    project=project,
                    standard_category=standard_categories[row['standard_category']],
                    sub_category=sub_categories[row['sub_category']],
                    category=categories[row['category']],
                    standard_category_name=standard_categories[row['standard_category']].name,
                    sub_category_name=sub_categories[row['sub_category']].name,
                    category_name=categories[row['category']].name,
                    geom=GEOSGeometry(row['geometry'].wkt),
                    created_by=user,
                    is_display=row['is_display'],
                )

                for _, row in gdf_linestring.iterrows()
            ]

            LineStringData.objects.bulk_create(linestring_data_list)
            end_time = time.time()
            execution_time = end_time - start_time
            print(
                f'Time taken to upload LineString {len(gdf_linestring)} the code: {execution_time} seconds')

            # For Point
            names_to_filter_point = []
            for item in filtered_result[2]:
                names_to_filter_point.append(
                    item.get('cleaned_name'))

            gdf_point = df[df['cleaned_name'].isin(names_to_filter_point)]
            gdf_point = gdf_point.copy()
            gdf_point['project'] = request.data.get('project_id')
            gdf_point['client'] = request.data.get('client_id')
            gdf_point['client'] = gdf_point['client'].astype('Int64')
            gdf_point['project'] = gdf_point['project'].astype('Int64')
            gdf_point = gdf_point.loc[gdf_point.geometry.type.isin(
                ["MultiPoint", "Point"])]

            def create_category_point(name):
                for i in filtered_result[2]:
                    if i.get('cleaned_name') == name:
                        return i.get('matched_category')

            gdf_point['category'] = gdf_point.apply(lambda row: create_category_point(
                row['cleaned_name']), axis=1)
            gdf_point['category'] = gdf_point['category'].astype('Int64')
            gdf_point['standard_category'] = gdf_point['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.id)
            gdf_point['standard_category'] = gdf_point['standard_category'].astype(
                'Int64')
            gdf_point['sub_category'] = gdf_point['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.id)
            gdf_point['sub_category'] = gdf_point['sub_category'].astype(
                'Int64')
            gdf_point['standard_category_name'] = gdf_point['category'].map(
                lambda x: Category.objects.get(id=x).standard_category.name)
            gdf_point['sub_category_name'] = gdf_point['category'].map(
                lambda x: Category.objects.get(id=x).sub_category.name)
            gdf_point['category_name'] = gdf_point['category'].map(
                lambda x: Category.objects.get(id=x).name)
            gdf_point['created_by'] = request.data.get('user_id')
            gdf_point['is_display'] = True

            print(gdf_point[[
                'project', 'client', 'standard_category', 'sub_category', 'category', 'standard_category_name', 'sub_category_name', 'category_name', 'created_by', 'is_display']].head(15))
            print(len(gdf_point), 'length of gdf_point')
            gdf_point = gdf_point.explode(ignore_index=True)
            print(len(gdf_point), 'length of gdf_point after explode')

            start_time = time.time()
            point_data_list = [
                PointData(
                    client=client,
                    project=project,
                    standard_category=standard_categories[row['standard_category']],
                    sub_category=sub_categories[row['sub_category']],
                    category=categories[row['category']],
                    standard_category_name=standard_categories[row['standard_category']].name,
                    sub_category_name=sub_categories[row['sub_category']].name,
                    category_name=categories[row['category']].name,
                    geom=GEOSGeometry(row['geometry'].wkt),
                    created_by=user,
                    is_display=row['is_display'],
                )

                for _, row in gdf_point.iterrows()
            ]

            PointData.objects.bulk_create(point_data_list)
            end_time = time.time()
            execution_time = end_time - start_time
            print(
                f'Time taken to upload Point {len(gdf_point)} the code: {execution_time} seconds')

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

        project_id = request.query_params.get('project')
        client_id = request.query_params.get('client')

        project = Project.objects.get(id=project_id)
        client = Client.objects.get(id=client_id)

        line_string_data = LineStringData.objects.filter(
            project_id=project_id, client_id=client_id
        )
        point_data = PointData.objects.filter(
            project_id=project_id, client_id=client_id)
        polygon_data = PolygonData.objects.filter(
            project_id=project_id, client_id=client_id)

        categories = Category.objects.filter(
            client=client
        ).values('id', 'type_of_geometry', 'view_name', 'description', 'name')

        for category in categories:
            style = CategoryStyle.objects.get(category=category['id'])

            # if category['type_of_geometry'] == "LineString":
            #     category['label'] = category['name']
            #     category['name'] = category['view_name']
            #     category['length'] = np.random.randint(100, 1000)
            #     category['area'] = 0
            #     category['count'] = line_string_data.filter(
            #         category=category['id']).count()
            #     category['value'] = line_string_data.filter(
            #         category=category['id']).count()
            #     category['symbol'] = {"color": style.fill,
            #                           "type_of_geometry": "LineString"}
            #     category['color'] = style.fill

            # if category['type_of_geometry'] == "Point":
            #     category['label'] = category['name']
            #     category['name'] = category['view_name']
            #     category['length'] = 0
            #     category['area'] = 0
            #     category['count'] = point_data.filter(
            #         category=category['id']).count()
            #     category['value'] = point_data.filter(
            #         category=category['id']).count()

            #     category['symbol'] = {"color": style.fill,
            #                           "type_of_geometry": "Point"}
            #     category['color'] = style.fill

            # Pie Chart only for polygon
            if category['type_of_geometry'] == "Polygon":
                category['label'] = category['name']
                category['value'] = 0
                category['symbol'] = {"color": style.fill,
                                      "type_of_geometry": "Polygon"}
                category['color'] = style.fill

        return Response({"rows": categories})


# For Inspection Types
class StandardInspectionViewSet(viewsets.ModelViewSet):
    queryset = StandardInspection.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = StandardInspectionSerializer
    pagination_class = None


class SubInspectionViewSet(viewsets.ModelViewSet):
    queryset = SubInspection.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = SubInspectionSerializer
    # filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ['standard_inspection']
    pagination_class = None


class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = InspectionSerializer
    # filter_backends = [DjangoFilterBackend,]
    # filterset_fields = ['sub_inspection']
    pagination_class = None


# For inspection reporting
class InspectionReportViewSet(viewsets.ModelViewSet):
    queryset = InspectionReport.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = InspectionReportSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['project']
    pagination_class = None


class InspectionPhotoViewSet(viewsets.ModelViewSet):
    queryset = InspectionPhoto.objects.filter(
        is_deleted=False).order_by('-created_at')
    serializer_class = InspectionPhotoSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['inspection_report', 'is_inspected']
    pagination_class = None


class InpsectionPhotoGeometryViewSet(viewsets.ModelViewSet):
    queryset = InpsectionPhotoGeometry.objects.filter(
        is_deleted=False).order_by('created_at')
    serializer_class = InpsectionPhotoGeometrySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['inspection_photo',
                        'standard_inspection', 'sub_inspection', 'inspection']
    pagination_class = None


class CategoryBoundingBoxViewSet(APIView):
    def get(self, request):

        return Response("Testing the API")

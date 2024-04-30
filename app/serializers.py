from rest_framework import serializers
from django.contrib.gis.db.models import Extent
from django.contrib.auth.models import User
from .models import Client, Project, ProjectPolygon, GlobalStandardCategory, GlobalSubCategory, GlobalCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData, LineStringData, PointData
from .models import RasterData
from .models import Role
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import StandardInspection, SubInspection, Inspection
from .models import InspectionReport, InspectionPhoto, InpsectionPhotoGeometry
from .models import MeasuringFileUpload
from django.contrib.auth.models import Group
import json
from shapely.wkt import loads


class UserSerializer(serializers.ModelSerializer):
    # role_name = serializers.SerializerMethodField('get_role_name')

    # def get_role_name(self, obj):
    #     user_role = UserRole.objects.get(user=obj)
    #     return str(user_role.role.name)
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'id',
                  'first_name', 'last_name', 'date_joined', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_client_name')
    show_eye_button = serializers.SerializerMethodField('get_show_area')

    def get_client_name(self, obj):
        client_name = obj.client.name
        return client_name

    def get_show_area(self, obj):
        return True

    class Meta:
        model = Project
        fields = "__all__"


class ProjectPolygonGeojsonSerializer(GeoFeatureModelSerializer):
    component = serializers.SerializerMethodField('get_component')
    project_polygon_id = serializers.SerializerMethodField('get_project_id')
    view_name = serializers.SerializerMethodField('get_view_name')

    def get_component(self, obj):
        return "project"

    def get_project_id(self, obj):
        return obj.id

    def get_view_name(self, obj):
        return json.loads(obj.attributes).get('name')

    class Meta:
        model = ProjectPolygon
        geo_field = "geom"
        fields = "__all__"


class RasterDataSerializer (serializers.ModelSerializer):
    path_of_file = serializers.SerializerMethodField('get_path_of_file')
    client_name = serializers.SerializerMethodField('get_client_name')
    project_name = serializers.SerializerMethodField('get_project_name')

    def get_path_of_file(self, obj):
        return str(obj.tif_file)

    def get_client_name(self, obj):
        client_name = obj.client.name
        return client_name

    def get_project_name(self, obj):
        project_name = obj.project.name
        return project_name

    class Meta:
        model = RasterData
        fields = "__all__"


# For Global Categoriess
class GlobalStandardCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.name
        return full_name

    class Meta:
        model = GlobalStandardCategory
        fields = "__all__"


class GlobalSubCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField(
        'get_standard_category_name')

    def get_full_name(self, obj):
        full_name = obj.standard_category.name + " | " + obj.name
        return full_name

    def get_standard_category_name(self, obj):
        standard_category_name = obj.standard_category.name
        return standard_category_name

    class Meta:
        model = GlobalSubCategory
        fields = "__all__"


class GlobalCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField(
        'get_standard_category_name')
    sub_category_name = serializers.SerializerMethodField(
        'get_sub_category_name')

    def get_full_name(self, obj):
        full_name = obj.sub_category.standard_category.name + \
            " | " + obj.sub_category.name + " | " + obj.name
        return full_name

    def get_standard_category_name(self, obj):
        standard_category_name = obj.sub_category.standard_category.name
        return standard_category_name

    def get_sub_category_name(self, obj):
        sub_category_name = obj.standard_category.name + " | " + obj.sub_category.name
        return sub_category_name

    class Meta:
        model = GlobalCategory
        fields = "__all__"


class GlobalCategoryStyleSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.category.sub_category.standard_category.name + \
            " | " + obj.category.sub_category.name + " | " + obj.category.name
        return full_name

    class Meta:
        model = GlobalCategoryStyle
        fields = "__all__"


# For project Categories
class StandardCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.name
        return full_name

    class Meta:
        model = StandardCategory
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField(
        'get_standard_category_name')

    def get_standard_category_name(self, obj):
        standard_category_name = obj.standard_category.name
        return standard_category_name

    def get_full_name(self, obj):
        full_name = obj.standard_category.name + " | " + obj.name
        return full_name

    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField(
        'get_standard_category_name')
    sub_category_name = serializers.SerializerMethodField(
        'get_sub_category_name')

    def get_full_name(self, obj):
        full_name = obj.sub_category.standard_category.name + \
            " | " + obj.sub_category.name + " | " + obj.name
        return full_name

    def get_standard_category_name(self, obj):
        standard_category_name = obj.sub_category.standard_category.name
        return standard_category_name

    def get_sub_category_name(self, obj):
        sub_category_name = obj.sub_category.name
        return sub_category_name

    class Meta:
        model = Category
        fields = "__all__"


class CategoryStyleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.category.sub_category.standard_category.name + \
            " | " + obj.category.sub_category.name + " | " + obj.category.name
        return full_name

    class Meta:
        model = CategoryStyle
        fields = "__all__"


# For Polygon
class PolygonDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = PolygonData
        fields = "__all__"

# For LineString


class LineStringDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = LineStringData
        fields = "__all__"


# For Point
class PointDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = PointData
        fields = "__all__"


class CategoryControlSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField('get_label')
    checked = serializers.SerializerMethodField('get_checked')
    extent = serializers.SerializerMethodField('get_extent')
    fill_opacity = serializers.SerializerMethodField('get_fill_opacity')
    fill_color = serializers.SerializerMethodField('get_fill_color')

    def get_label(self, obj):
        return obj.name

    def get_checked(self, obj):
        return False

    def get_extent(self, obj):
        if obj.type_of_geometry == "Polygon":
            extent = PolygonData.objects.filter(
                category=obj.id).aggregate(extent=Extent('geom'))
            return extent
        if obj.type_of_geometry == "LineString":
            extent = LineStringData.objects.filter(
                category=obj.id).aggregate(extent=Extent('geom'))
            return extent
        if obj.type_of_geometry == "Point":
            extent = PointData.objects.filter(
                category=obj.id).aggregate(extent=Extent('geom'))
            return extent

        return []

    def get_fill_opacity(self, obj):
        category_style = CategoryStyle.objects.get(category=obj.id)
        return category_style.fill_opacity

    def get_fill_color(self, obj):
        category_style = CategoryStyle.objects.get(category=obj.id)
        return category_style.fill

    class Meta:
        model = Category
        fields = ['id', 'name', 'client', 'label',
                  'checked', 'extent', 'view_name', 'type_of_geometry', 'fill_opacity', 'fill_color',]


class SubCategoryControlSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField('get_label')
    checked = serializers.SerializerMethodField('get_checked')
    expand = serializers.SerializerMethodField('get_expand')
    indeterminate = serializers.SerializerMethodField('get_indeterminate')
    extent = serializers.SerializerMethodField('get_extent')
    category = serializers.SerializerMethodField('get_category')

    def get_label(self, obj):
        return obj.name

    def get_checked(self, obj):
        return False

    def get_expand(self, obj):
        return False

    def get_indeterminate(self, obj):
        return False

    def get_extent(self, obj):

        return []

    def get_category(self, obj):
        queryset = Category.objects.filter(
            sub_category=obj.id)
        serialized = CategoryControlSerializer(queryset, many=True)
        return serialized.data

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'client', 'label', 'checked', 'expand',
                  'indeterminate', 'extent', 'category', ]


class StandardCategoryControlSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField('get_label')
    checked = serializers.SerializerMethodField('get_checked')
    expand = serializers.SerializerMethodField('get_expand')
    indeterminate = serializers.SerializerMethodField('get_indeterminate')
    extent = serializers.SerializerMethodField('get_extent')
    sub_category = serializers.SerializerMethodField('get_sub_category')

    def get_label(self, obj):
        return obj.name

    def get_checked(self, obj):
        return False

    def get_expand(self, obj):
        return False

    def get_indeterminate(self, obj):
        return False

    def get_extent(self, obj):

        return []

    def get_sub_category(self, obj):
        print(dir(self), 'queryset')
        print(dir(obj))
        queryset = SubCategory.objects.filter(
            standard_category=obj.id)
        serialized = SubCategoryControlSerializer(queryset, many=True)
        return serialized.data

    class Meta:
        model = StandardCategory
        fields = ['id', 'name', 'client', 'label', 'checked', 'expand',
                  'indeterminate', 'extent', 'sub_category', ]


class PolygonDataGeojsonSerializer(GeoFeatureModelSerializer):
    property = serializers.SerializerMethodField('get_property')
    category = serializers.SerializerMethodField('get_category')
    category_id = serializers.SerializerMethodField('get_category_id')
    area = serializers.SerializerMethodField('get_area')
    perimeter = serializers.SerializerMethodField('get_perimeter')
    # centroid = serializers.SerializerMethodField('get_centroid')
    type_of_geometry = serializers.SerializerMethodField(
        'get_type_of_geometry')
    view_name = serializers.SerializerMethodField(
        'get_view_name')
    component = serializers.SerializerMethodField('get_component')

    def get_property(self, obj):
        return obj.project.name

    def get_category(self, obj):
        return obj.category.name

    def get_area(self, obj):
        obj.geom.transform(32633)
        return str(round(obj.geom.area, 2)) + " " + "meter square"

    def get_perimeter(self, obj):
        # print(dir(obj.geom.length))
        # return obj.geom.length
        obj.geom.transform(32633)
        return str(round(obj.geom.length, 2)) + " " + "meters"

    # def get_centroid(self, obj):
    #     # print(dir(obj.geom.length))
    #     # return obj.geom.length
    #     return str(obj.geom.centroid)
    def get_type_of_geometry(self, obj):
        return 'Polygon'

    def get_view_name(self, obj):
        return obj.category.view_name

    def get_category_id(self, obj):
        return obj.category.id

    def get_component(self, obj):
        return "category"

    class Meta:
        model = PolygonData
        geo_field = "geom"
        fields = ('id', 'property', 'category',
                  'area', 'perimeter', 'type_of_geometry', 'view_name', 'category_id', 'component')


class PointDataGeojsonSerializer(GeoFeatureModelSerializer):
    property = serializers.SerializerMethodField('get_property')
    category = serializers.SerializerMethodField('get_category')
    category_id = serializers.SerializerMethodField('get_category_id')
    type_of_geometry = serializers.SerializerMethodField(
        'get_type_of_geometry')
    view_name = serializers.SerializerMethodField(
        'get_view_name')
    component = serializers.SerializerMethodField('get_component')

    def get_property(self, obj):
        return obj.project.name

    def get_category(self, obj):
        return obj.category.name

    def get_type_of_geometry(self, obj):
        return 'Point'

    def get_view_name(self, obj):
        return obj.category.view_name

    def get_category_id(self, obj):
        return obj.category.id

    def get_component(self, obj):
        return "category"

    class Meta:
        model = PointData
        geo_field = "geom"
        fields = ('id', 'property', 'category',
                  'type_of_geometry', 'view_name', 'category_id', 'component')


class LineStringDataGeojsonSerializer(GeoFeatureModelSerializer):
    property = serializers.SerializerMethodField('get_property')
    category = serializers.SerializerMethodField('get_category')
    category_id = serializers.SerializerMethodField('get_category_id')
    length = serializers.SerializerMethodField('get_length')
    type_of_geometry = serializers.SerializerMethodField(
        'get_type_of_geometry')
    view_name = serializers.SerializerMethodField(
        'get_view_name')
    component = serializers.SerializerMethodField('get_component')

    def get_property(self, obj):
        return obj.project.name

    def get_category(self, obj):
        return obj.category.name

    def get_length(self, obj):
        # print(dir(obj.geom.length))
        # return obj.geom.length
        obj.geom.transform(32633)
        return str(round(obj.geom.length, 2)) + " " + "meters"

    def get_type_of_geometry(self, obj):
        return 'LineString'

    def get_view_name(self, obj):
        return obj.category.view_name

    def get_category_id(self, obj):
        return obj.category.id

    def get_component(self, obj):
        return "category"

    class Meta:
        model = LineStringData
        geo_field = "geom"
        fields = ('id', 'property', 'category',
                  'length', 'type_of_geometry', 'view_name', 'category_id', 'component')


# For Inspection types
class StandardInspectionSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.name
        return full_name

    class Meta:
        model = StandardInspection
        fields = "__all__"


class SubInspectionSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):

        return obj.name

    class Meta:
        model = SubInspection
        fields = "__all__"


class InspectionSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):

        return obj.name

    class Meta:
        model = Inspection
        fields = "__all__"


# For inspection reporting

class InspectionReportSerializer(serializers.ModelSerializer):
    total_photos = serializers.SerializerMethodField('get_total_photos')
    inspected_photos = serializers.SerializerMethodField(
        'get_inspected_photos')

    def get_total_photos(self, obj):
        total_photos = InspectionPhoto.objects.filter(
            inspection_report=obj.id).count()
        return total_photos

    def get_inspected_photos(self, obj):
        inspected_photos = InspectionPhoto.objects.filter(
            inspection_report=obj.id, is_inspected=True).count()
        return inspected_photos

    class Meta:
        model = InspectionReport
        fields = "__all__"


class InspectionPhotoSerializer(serializers.ModelSerializer):
    selected = serializers.SerializerMethodField('get_selected')

    def get_selected(self, obj):
        return False

    class Meta:
        model = InspectionPhoto
        fields = "__all__"


class InpsectionPhotoGeometrySerializer(serializers.ModelSerializer):
    standard_inspection_name = serializers.SerializerMethodField(
        'get_standard_inspection_name')
    sub_inspection_name = serializers.SerializerMethodField(
        'get_sub_inspection_name')
    inspection_name = serializers.SerializerMethodField('get_inspection_name')

    def get_standard_inspection_name(self, obj):
        return obj.standard_inspection.name

    def get_sub_inspection_name(self, obj):
        return obj.sub_inspection.name

    def get_inspection_name(self, obj):
        return obj.inspection.name

    class Meta:
        model = InpsectionPhotoGeometry
        fields = "__all__"


# Its show the status of the file upload
class MeasuringFileUploadSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_client_name')
    project_name = serializers.SerializerMethodField('get_project_name')

    def get_client_name(self, obj):
        client_name = obj.client.name
        return client_name

    def get_project_name(self, obj):
        project_name = obj.project.name
        return project_name

    class Meta:
        model = MeasuringFileUpload
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


# For Roles
class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permissions')
    group_name = serializers.SerializerMethodField('get_group_name')
    user_name = serializers.SerializerMethodField('get_user_name')
    email = serializers.SerializerMethodField('get_email')

    def get_permissions(self, obj):
        return obj.group.permissions.values_list('codename', flat=True)

    def get_group_name(self, obj):
        return obj.group.name

    def get_user_name(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Role
        fields = "__all__"


class RoleSerializerForProjects(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permissions')
    group_name = serializers.SerializerMethodField('get_group_name')
    user_name = serializers.SerializerMethodField('get_user_name')
    email = serializers.SerializerMethodField('get_email')
    project = ProjectSerializer(many=True)

    def get_permissions(self, obj):
        return obj.group.permissions.values_list('codename', flat=True)

    def get_group_name(self, obj):
        return obj.group.name

    def get_user_name(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Role
        fields = "__all__"

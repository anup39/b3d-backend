from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project, GlobalStandardCategory, GlobalSubCategory, GlobalCategory, GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category, CategoryStyle
from .models import PolygonData
from .models import RasterData
from .models import Role, UserRole
from django.db import connection


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

    def get_client_name(self, obj):
        client_name = obj.client.name
        return client_name

    class Meta:
        model = Project
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

    def get_full_name(self, obj):
        full_name = obj.sub_category.standard_category.name + \
            " | " + obj.sub_category.name + " | " + obj.name
        return full_name

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


# For Roles
class RoleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.name
        return full_name

    class Meta:
        model = Role
        fields = "__all__"


class UserRoleSerializer(serializers.ModelSerializer):

    role_name = serializers.SerializerMethodField('get_role_name')
    username = serializers.SerializerMethodField('get_username')
    email = serializers.SerializerMethodField('get_email')
    date_joined = serializers.SerializerMethodField('get_date_joined')

    def get_role_name(self, obj):
        return str(obj.role.name)

    def get_username(self, obj):
        return str(obj.user.username)

    def get_email(self, obj):
        return str(obj.user.email)

    def get_date_joined(self, obj):
        return str(obj.user.date_joined)

    class Meta:
        model = UserRole
        fields = "__all__"


class CategoryControlSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField('get_label')
    checked = serializers.SerializerMethodField('get_checked')
    extent = serializers.SerializerMethodField('get_extent')

    def get_label(self, obj):
        return obj.name

    def get_checked(self, obj):
        return False

    def get_extent(self, obj):
        categroy_id = obj.id
        query = f'''
            SELECT 
            ST_Extent(extent) AS combined_extent
            FROM(
                SELECT 
                    'app_point' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_pointdata
                WHERE 
                    category_id = '{categroy_id}'

                UNION ALL

                SELECT 
                    'app_polygondata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_polygondata
                WHERE 
                    category_id = '{categroy_id}'

                UNION ALL

                SELECT 
                    'app_linestringdata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_linestringdata
                WHERE 
                    category_id = '{categroy_id}'
            ) AS combined_extents;
        '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'client', 'label',
                  'checked', 'extent', 'view_name']


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
        sub_categroy_id = obj.id
        query = f'''
            SELECT 
            ST_Extent(extent) AS combined_extent
            FROM(
                SELECT 
                    'app_point' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_pointdata
                WHERE 
                    sub_category_id = '{sub_categroy_id}'

                UNION ALL

                SELECT 
                    'app_polygondata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_polygondata
                WHERE 
                    sub_category_id = '{sub_categroy_id}'

                UNION ALL

                SELECT 
                    'app_linestringdata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_linestringdata
                WHERE 
                    sub_category_id = '{sub_categroy_id}'
            ) AS combined_extents;
        '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results

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
        standard_categroy_id = obj.id
        query = f'''
            SELECT 
            ST_Extent(extent) AS combined_extent
            FROM(
                SELECT 
                    'app_point' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_pointdata
                WHERE 
                    standard_category_id = '{standard_categroy_id}'

                UNION ALL

                SELECT 
                    'app_polygondata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_polygondata
                WHERE 
                    standard_category_id = '{standard_categroy_id}'

                UNION ALL

                SELECT 
                    'app_linestringdata' AS table_name,
                    ST_Extent(geom) AS extent
                FROM 
                    app_linestringdata
                WHERE 
                    standard_category_id = '{standard_categroy_id}'
            ) AS combined_extents;
        '''

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results

    def get_sub_category(self, obj):
        queryset = SubCategory.objects.filter(
            standard_category=obj.id)
        serialized = SubCategoryControlSerializer(queryset, many=True)
        return serialized.data

    class Meta:
        model = StandardCategory
        fields = ['id', 'name', 'client', 'label', 'checked', 'expand',
                  'indeterminate', 'extent', 'sub_category', ]

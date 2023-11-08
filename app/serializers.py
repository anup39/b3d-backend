from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project ,GlobalStandardCategory, GlobalSubCategory, GlobalCategory ,GlobalCategoryStyle
from .models import StandardCategory, SubCategory, Category ,CategoryStyle
from .models import PolygonData
from .models import RasterData
from .models import Role, UserRole


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields="__all__"


# For Global Categoriess
class GlobalStandardCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name =  obj.name
        return full_name
    class Meta:
        model = GlobalStandardCategory
        fields = "__all__"


class GlobalSubCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField('get_standard_category_name')


    def get_full_name(self, obj):
        full_name = obj.standard_category.name +" | "+ obj.name
        return full_name
    
    def get_standard_category_name(self,obj):
        standard_category_name = obj.standard_category.name
        return standard_category_name
    class Meta:
        model = GlobalSubCategory
        fields = "__all__"

class GlobalCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField('get_standard_category_name')
    sub_category_name = serializers.SerializerMethodField('get_sub_category_name')



    def get_full_name(self, obj):
        full_name = obj.sub_category.standard_category.name + " | " + obj.sub_category.name + " | " + obj.name
        return full_name
    
    def get_standard_category_name(self,obj):
        standard_category_name = obj.sub_category.standard_category.name
        return standard_category_name
    
    def get_sub_category_name(self,obj):
        sub_category_name = obj.standard_category.name + " | " + obj.sub_category.name
        return sub_category_name

    class Meta:
        model = GlobalCategory
        fields = "__all__"

class GlobalCategoryStyleSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name =  obj.category.sub_category.standard_category.name + " | " + obj.category.sub_category.name + " | " + obj.category.name
        return full_name

    class Meta:
        model = GlobalCategoryStyle
        fields = "__all__"


# For project Categories
class StandardCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name =  obj.name
        return full_name

    class Meta:
        model = StandardCategory
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')
    standard_category_name = serializers.SerializerMethodField('get_standard_category_name')

    def get_standard_category_name(self,obj):
        standard_category_name = obj.standard_category.name
        return standard_category_name

    def get_full_name(self, obj):
        full_name = obj.standard_category.name +" | "+ obj.name
        return full_name

    class Meta:
        model = SubCategory
        fields = "__all__"



class CategorySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name = obj.sub_category.standard_category.name + " | " + obj.sub_category.name + " | " + obj.name
        return full_name

    class Meta:
        model = Category
        fields = "__all__"


class CategoryStyleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        full_name =  obj.category.sub_category.standard_category.name + " | " + obj.category.sub_category.name + " | " + obj.category.name
        return full_name

    class Meta:
        model = CategoryStyle
        fields = "__all__"


# For Polygon 
class PolygonDataSerializer (serializers.ModelSerializer):
    class Meta:
        model=PolygonData
        fields="__all__"


class RasterDataSerializer (serializers.ModelSerializer):
    path_of_file = serializers.SerializerMethodField('get_path_of_file')

    def get_path_of_file(self,obj):
        return str(obj.tif_file)
    
    class Meta:
        model=RasterData
        fields="__all__"


#For Roles
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields="__all__"


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserRole
        fields="__all__"
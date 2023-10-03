from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project ,GlobalStandardCategory, GlobalSubCategory, GlobalCategory ,GlobalCategoryStyle



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


class GlobalStandardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalStandardCategory
        fields = "__all__"


class GlobalSubCategorySerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField('get_fullname')

    def get_fullname(self, obj):
        full_name = obj.standard_category.name +"|"+ obj.name
        return full_name
    class Meta:
        model = GlobalSubCategory
        fields = "__all__"

class GlobalCategorySerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField('get_fullname')

    def get_fullname(self, obj):
        full_name = obj.sub_category.standard_category.name + "|" + obj.sub_category.name + "|" + obj.name
        return full_name

    class Meta:
        model = GlobalCategory
        fields = "__all__"

class GlobalCategoryStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalCategoryStyle
        fields = "__all__"


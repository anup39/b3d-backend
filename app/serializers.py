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
    class Meta:
        model = GlobalSubCategory
        fields = "__all__"

class GlobalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalCategory
        fields = "__all__"

class GlobalCategoryStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalCategoryStyle
        fields = "__all__"


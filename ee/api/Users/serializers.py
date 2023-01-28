from rest_framework import serializers
from .models import ImageUpload, UserProfile, User
from drf_writable_nested import WritableNestedModelSerializer
from django.urls import reverse

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('image',)


class UserProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    picture = ImageUploadSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ('picture', 'date_of_birth', 'phone', 'code_country')


class UserSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('user_profile', 'email', 'first_name', 'last_name')



    
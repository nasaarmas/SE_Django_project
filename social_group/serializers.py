from rest_framework import serializers
from .models import SocialGroupMember, SocialGroup, SocialGroupPost


class SocialGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroup
        fields = ['id', 'name', 'description', 'created_at']


class SocialGroupMemberSerializer(serializers.ModelSerializer):
    social_group = serializers.PrimaryKeyRelatedField(queryset=SocialGroup.objects.all())

    class Meta:
        model = SocialGroupMember
        fields = ['id', 'date_joined', 'date_left', 'role', 'social_group', 'user']


class SocialGroupsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialGroupPost
        fields = ['id', 'social_group', 'user', 'content', 'created_at', 'updated_at', 'media']


class SocialGroupUsersSerializer(serializers.ModelSerializer):
    social_group = serializers.PrimaryKeyRelatedField(queryset=SocialGroup.objects.all())

    class Meta:
        model = SocialGroupMember
        fields = ['id', 'date_joined', 'date_left', 'role', 'social_group', 'user']

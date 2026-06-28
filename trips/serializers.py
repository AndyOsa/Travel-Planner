from rest_framework import serializers
from .models import Project, Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'title', 'notes', 'visited', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_completed(self, obj):
        return obj.is_completed()


class ProjectCreateSerializer(serializers.ModelSerializer):
    places = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'places']
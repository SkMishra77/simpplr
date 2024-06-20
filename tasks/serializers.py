from rest_framework import serializers

from .models import *


class MovieViewSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name')

    class Meta:
        model = MovieModel
        fields = ['id', 'name', 'director', 'release_year', 'language', 'language_name', 'rating']


class MovieCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ['name', 'director', 'release_year', 'language', 'rating']


class MovieUpdationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = ['name', 'director', 'release_year', 'language', 'rating']


class MovieUpdationRequest(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(read_only=True)
    director = serializers.CharField(read_only=True)
    release_year = serializers.IntegerField(read_only=True)
    language = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)


class LanguageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = '__all__'

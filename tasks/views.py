from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from simpplr.utils import response_fun, MyPaginator
from .serializers import *


class MovieViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items per page",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search term to filter movies",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by movie name", type=openapi.TYPE_STRING),
            openapi.Parameter('director', openapi.IN_QUERY, description="Filter by movie director",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('release_year', openapi.IN_QUERY, description="Filter by release year",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Filter by movie language",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('rating', openapi.IN_QUERY, description="Filter by movie rating",
                              type=openapi.TYPE_NUMBER),
        ],
        operation_summary="Retrieve movies list",
        operation_description="This endpoint allows users to retrieve a list of movies with optional search and "
                              "filter parameters. The results are paginated.",
    )
    def get_movies(self, request):
        search: str = request.GET.get('search', '')
        name = request.GET.get('name')
        director = request.GET.get('director')
        release_year = request.GET.get('release_year')
        language = request.GET.get('language')
        rating = request.GET.get('rating')

        # Search
        if not search or search == '':
            objects = MovieModel.objects.all().order_by('-created_at')
        else:
            search = search.strip()
            objects = MovieModel.objects.filter(
                Q(name__icontains=search)
            ).order_by('-created_at')

        # Filters
        if name:
            objects = objects.filter(Q(name__icontains=name))
        if director:
            objects = objects.filter(Q(director__icontains=director))
        if release_year:
            objects = objects.filter(Q(release_year=release_year))
        if language:
            objects = objects.filter(Q(language__name__icontains=language))
        if rating:
            objects = objects.filter(Q(rating=rating))

        paginator = MyPaginator()
        result_page = paginator.paginate_queryset(objects, request)
        serializer = MovieViewSerializer(result_page, many=True)
        data = paginator.get_paginated_response(serializer.data).data
        return response_fun(1, data)

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the movie'),
                'director': openapi.Schema(type=openapi.TYPE_STRING, description='Director of the movie'),
                'release_year': openapi.Schema(type=openapi.TYPE_INTEGER, description='Release year of the movie',
                                               maximum=9999, minimum=1000),
                'language': openapi.Schema(type=openapi.TYPE_STRING, description='Language of the movie'),
                'rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='Rating of the movie', minimum=0,
                                         maximum=10.0),
            },
            required=['name', 'director', 'release_year', 'language', 'rating']
        ),
        operation_summary="Add a new movie",
        operation_description="This endpoint allows users to add a new movie by providing the necessary details such "
                              "as name, director, release year, language, and rating.Language code should need to be "
                              "entered according to the response of `get_language_codes` Endpoint"
    )
    def add_movie(self, request):
        data = request.data
        serializer = MovieCreationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_fun(1, "Data Added Successfully")

    @action(detail=False, methods=['PATCH'])
    @swagger_auto_schema(
        operation_id="update_movie",
        operation_summary="Updates a Movie Entry",
        operation_description="This endpoint allows you to partially update a specific movie record in the database. "
                              "Provide the movie's ID and the desired changes in the request body using the "
                              "`MovieUpdationRequest` schema.",
        request_body=MovieUpdationRequest)
    def update_movie(self, request):
        data = request.data
        _id = data.get('id')
        if not _id:
            return response_fun(0, "Id not Found")

        _object = MovieModel.objects.filter(
            pk=_id
        ).first()

        if not _object:
            return response_fun(0, "Entry Not Found")

        serializer = MovieCreationSerializer(_object, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response_fun(1, "Data Updated Successfully")

    @action(detail=False, methods=['DELETE'])
    @swagger_auto_schema(
        operation_id="delete_movie",
        operation_summary="Deletes a Movie Entry",
        operation_description="This endpoint allows you to delete a specific movie record from the database. Provide "
                              "the movie's ID in the query parameter 'id' to perform the deletion.",
        # Detailed description
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="The unique identifier of the movie to be deleted. (Required)",
                required=True
            )
        ], )
    def delete_movie(self, request):
        _id = request.GET.get('id')
        if not _id:
            return response_fun(0, "Id not Found")

        _object: MovieModel = MovieModel.objects.filter(
            pk=_id
        ).first()
        if not _object:
            return response_fun(0, "Entry Not Found")

        _object.delete()
        return response_fun(1, "Data Deleted Successfully")

    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        operation_id="get_language_codes",
        operation_summary="Retrieves All Language Codes",
        operation_description="This endpoint fetches a list of all available language codes stored in the database."
    )
    def get_language_codes(self, request):
        lang_object = LanguageModel.objects.all()
        data = LanguageViewSerializer(lang_object, many=True).data
        return response_fun(1, data)

    @action(detail=False, methods=['GET'])
    @swagger_auto_schema(
        operation_id="get_movies_count_by_language",
        operation_summary="Get Movie Count by Language Code",
        operation_description="This endpoint retrieves the number of movies associated with a specific language code. "
                              "Provide the 'language_code' query parameter to filter the results.",
        manual_parameters=[
            openapi.Parameter(
                name='language_code',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="The language code to filter movies by. (Required)",
                required=True
            )
        ]
    )
    def get_movies_count_by_language(self, request):
        language = request.GET.get('language_code')
        if not language:
            return response_fun(0, "Language Code not Found")

        language_object = LanguageModel.objects.filter(code=language).first()
        if not language_object:
            return response_fun(0, "Language Code not exists")

        count = MovieModel.objects.filter(
            language=language_object.pk
        ).count()

        return response_fun(1, {
            'count': count,
            'language': language_object.code,
        })

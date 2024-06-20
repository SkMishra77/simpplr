import os
from uuid import uuid4

from django.utils import timezone
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def getMovieImageName(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = str(uuid4().hex)
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_name = f"Image_{timestamp}_{unique_id}.{ext}"
    return os.path.join(f'movie_images', unique_name)


def response_fun(*args, status_code=None):
    if status_code:
        return Response({'error': True, 'message': args[1], 'status_code': status_code})
    if args[0] == 1:
        return Response({'error': False, 'responseData': args[1], 'status_code': status.HTTP_200_OK})
    else:
        return Response(
            {'error': True, 'message': args[1], 'status_code': status.HTTP_400_BAD_REQUEST})


class MyPaginator(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'limit'
    max_page_size = 100

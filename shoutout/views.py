from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


from .models import Shoutouts
from .serializers import ShoutoutSerializer

# add is_read 
@api_view(['GET'])
def shoutouts(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 7
        shoutout_objects = Shoutouts.objects.filter(is_read=False, is_published=True)
        result_page = paginator.paginate_queryset(shoutout_objects, request)
        serializer = ShoutoutSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response(status=status.HTTP_400_BAD_REQUEST)

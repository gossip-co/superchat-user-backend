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
        shoutout_objects = Shoutouts.objects.filter(is_published=True)
        result_page = paginator.paginate_queryset(shoutout_objects, request)
        serializer = ShoutoutSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as error:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shoutouts_ready_to_read(request):
    try:
        shoutout_object = Shoutouts.objects.filter(is_read=False, is_published=True)
        serializer = ShoutoutSerializer(shoutout_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_shoutout(request):
    try:
        data = request.data
        shoutout_id = data["shoutout_id"]

        shoutout_object = Shoutouts.objects.get(pk=shoutout_id)
        shoutout_object.is_read = True
        shoutout_object.save()
        return Response({"message": "shoutout updated"}, status=status.HTTP_200_OK)

    except Exception as error:
        print("ERROR", error)
        return Response({"message": "server error"}, status=status.HTTP_400_BAD_REQUEST)

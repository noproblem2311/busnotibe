import uuid
from src.models import Request
from src.serializers.Request.RequestSerializer import RequestSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class RequestListView(APIView):
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        child_data = request.data
        child_data['id'] = str(uuid.uuid4())
        child_data['status'] = 'pending'
        serializer = RequestSerializer(data=child_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDetailView(APIView):
    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return None

    def get(self, request, pk):
        request_obj = self.get_object(pk)
        if request_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RequestSerializer(request_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        request_obj = self.get_object(pk)
        if request_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RequestSerializer(request_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        request_obj = self.get_object(pk)
        if request_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RequestSerializer(request_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        request_obj = self.get_object(pk)
        if request_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_request_by_parent_id(request, pk):
    if request.method == 'GET':
        parentid = pk
        requests = Request.objects.filter(parent_id=parentid)
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
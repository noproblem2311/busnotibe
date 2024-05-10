import uuid
from src.models import Child
from src.serializers.Child.ChildSerializer import ChildSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class ChildListView(APIView):
    def get(self, request):
        children = Child.objects.all()
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    def post(self, request):
        child_data= request.data
        child_data['id'] = str(uuid.uuid4())
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildDetailView(APIView):
    def get_object(self, pk):
        try:
            return Child.objects.get(pk=pk)
        except Child.DoesNotExist:
            return None

    def get(self, request, pk):
        child = self.get_object(pk)
        if child is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(child)
        return Response(serializer.data)

    def put(self, request, pk):
        child = self.get_object(pk)
        if child is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        child = self.get_object(pk)
        if child is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ChildSerializer(child, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        child = self.get_object(pk)
        if child is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        child.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_child_by_parent_id(request, pk):
    if request.method == 'GET':
        parentid = pk
        children = Child.objects.filter(parent_id=parentid)
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

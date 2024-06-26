from src.models import Parent
from src.serializers.Parent.ParentSerializer import ParentSerializer
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ParentListView(APIView):
    def get(self, request):
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            return None

    def get(self, request, pk):
        parent = self.get_object(pk)
        if parent is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)

    def put(self, request, pk):
        parent = self.get_object(pk)
        if parent is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParentSerializer(parent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        parent = self.get_object(pk)
        if parent is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ParentSerializer(parent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        parent = self.get_object(pk)
        if parent is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        parent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def search_requests_parent(request):
    field = request.query_params.get('field')
    key = request.query_params.get('key')

    # List of allowed fields for searching
    allowed_fields = {
       'id', 'user_name', 'email','date_of_birth', 'language'
    }

    if not field or not key:
        return Response({'detail': 'Field and key parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    if field not in allowed_fields:
        return Response({'detail': f'Invalid field parameter: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Use __icontains for text fields to allow partial matching
    query_filter = {f"{field}__icontains": key}
    requests = Parent.objects.filter(**query_filter)
    serializer = ParentSerializer(requests, many=True)
    return Response(serializer.data)
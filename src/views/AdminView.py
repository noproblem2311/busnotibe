

import uuid
from src.models import Admin
from src.serializers.Admin.AdminSerializer import AdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class AdminListView(APIView):
    def get(self, request):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDetailView(APIView):
    def get_object(self, pk):
        try:
            return Admin.objects.get(pk=pk)
        except Admin.DoesNotExist:
            return None

    def get(self, request, pk):
        admin = self.get_object(pk)
        if admin is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminSerializer(admin)
        return Response(serializer.data)

    def put(self, request, pk):
        admin = self.get_object(pk)
        if admin is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminSerializer(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        admin = self.get_object(pk)
        if admin is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        admin = self.get_object(pk)
        if admin is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

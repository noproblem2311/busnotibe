from src.models import School
from src.serializers.School.SchoolSerializer import SchoolSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



import uuid





class SchoolListView(APIView):
    def get(self, request):
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

    def post(self, request):
        school_data= request.data
        school_data['id'] = str(uuid.uuid4())
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolDetailView(APIView):
    def get_object(self, pk):
        try:
            return School.objects.get(pk=pk)
        except School.DoesNotExist:
            return None

    def get(self, request, pk):
        school = self.get_object(pk)
        if school is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)

    def put(self, request, pk):
        school = self.get_object(pk)
        if school is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        school = self.get_object(pk)
        if school is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(school, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        school = self.get_object(pk)
        if school is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from src.models import Template
from src.serializers.Template.TemplateSerializer import TemplateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TemplateListView(APIView):
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetailView(APIView):
    def get_object(self, pk):
        try:
            return Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return None

    def get(self, request, pk):
        template_obj = self.get_object(pk)
        if template_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template_obj)
        return Response(serializer.data)

    def put(self, request, pk):
        template_obj = self.get_object(pk)
        if template_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        template_obj = self.get_object(pk)
        if template_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        template_obj = self.get_object(pk)
        if template_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        template_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

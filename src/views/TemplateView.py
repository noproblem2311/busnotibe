import uuid
from src.models import Template
from src.serializers.Template.TemplateSerializer import TemplateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class TemplateListView(APIView):
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        datacurrent = request.data
        datacurrent['id'] = str(uuid.uuid4())
        serializer = TemplateSerializer(data=datacurrent)
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



@api_view(['GET'])
def search_requests_template(request):
    field = request.query_params.get('field')
    key = request.query_params.get('key')

    # List of allowed fields for searching
    allowed_fields = {
       'id', 'name', 'image', 'price'
    }

    if not field or not key:
        return Response({'detail': 'Field and key parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    if field not in allowed_fields:
        return Response({'detail': f'Invalid field parameter: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Use __icontains for text fields to allow partial matching
    query_filter = {f"{field}__icontains": key}
    requests = Template.objects.filter(**query_filter)
    serializer = TemplateSerializer(requests, many=True)
    return Response(serializer.data)
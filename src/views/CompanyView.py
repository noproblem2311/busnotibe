import uuid
from src.models.Company import Company
from src.serializers.Company.CompanySerializer import CompanySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        datacurrent= request.data
        datacurrent['id'] = str(uuid.uuid4())
        serializer = CompanySerializer(data=datacurrent)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailView(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return None

    def get(self, request, pk):
        company = self.get_object(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        company = self.get_object(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_object(pk)
        if company is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
@api_view(['GET'])
def search_requests_company(request):
    field = request.query_params.get('field')
    key = request.query_params.get('key')

    # List of allowed fields for searching
    allowed_fields = {
    'name_en', 'name_cn'
        }

    if not field or not key:
        return Response({'detail': 'Field and key parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    if field not in allowed_fields:
        return Response({'detail': f'Invalid field parameter: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Use __icontains for text fields to allow partial matching
    query_filter = {f"{field}__icontains": key}
    requests = Company.objects.filter(**query_filter)
    serializer = CompanySerializer(requests, many=True)
    return Response(serializer.data)
from src.models import Driver
from src.serializers.Driver.DriverSerializers import DriverSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class DriverListView(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DriverDetailView(APIView):
    def get_object(self, pk):
        try:
            return Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return None

    def get(self, request, pk):
        driver = self.get_object(pk)
        if driver is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def put(self, request, pk):
        driver = self.get_object(pk)
        if driver is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        driver = self.get_object(pk)
        if driver is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DriverSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        driver = self.get_object(pk)
        if driver is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
def search_requests_driver(request):
    field = request.query_params.get('field')
    key = request.query_params.get('key')

    # List of allowed fields for searching
    allowed_fields = {
       'id', 'user_name', 'email', 'phone_number', 'date_of_birth', 'company_id', 'license', 'bus_number', 'language'
    }

    if not field or not key:
        return Response({'detail': 'Field and key parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    if field not in allowed_fields:
        return Response({'detail': f'Invalid field parameter: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Use __icontains for text fields to allow partial matching
    query_filter = {f"{field}__icontains": key}
    requests = Driver.objects.filter(**query_filter)
    serializer = DriverSerializer(requests, many=True)
    return Response(serializer.data)
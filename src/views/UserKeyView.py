import uuid
from src.models import UserKey
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from src.helper.IsAuth import getUserId
from src.serializers.UserKey.UserKeySerializer import UserKeySerializer

class UserKeyView(APIView):
    def get(self, request):
        user_keys = UserKey.objects.all()
        serializer = UserKeySerializer(user_keys, many=True)
        return Response(serializer.data)
    def post(self, request):
        userid = getUserId(request)
        if userid == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        datacurrent = request.data
        datacurrent['id'] = str(uuid.uuid4())
        datacurrent['user_id'] = userid
        key = datacurrent['key']
        if key:
            try:
                UserKey.objects.filter(key=key).delete()
            except ObjectDoesNotExist:
                pass
        serializer = UserKeySerializer(data=datacurrent)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserKeyDetailView(APIView):
    def get_object(self, pk):
        try:
            return UserKey.objects.get(pk=pk)
        except UserKey.DoesNotExist:
            return None
    def get(self, request, pk):
        user_key = self.get_object(pk)
        if user_key is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserKeySerializer(user_key)
        return Response(serializer.data)
    def put(self, request, pk):
        user_key = self.get_object(pk)
        if user_key is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserKeySerializer(user_key, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user_key = self.get_object(pk)
        if user_key is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserKeySerializer(user_key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_key = self.get_object(pk)
        if user_key is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['DELETE'])
def delete_by_key(request, pk):
    key = pk
    try:
        # Attempt to delete the UserKey object
        allUserhaskey = UserKey.objects.filter(key=key)
        if allUserhaskey:
            allUserhaskey.delete()
        else:
            return Response(data="key not found" ,status=status.HTTP_404_NOT_FOUND)
        
        return Response(data="deleted successfully" ,status=status.HTTP_200_OK)
    except UserKey.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

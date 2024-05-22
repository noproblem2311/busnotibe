import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.models.Notification import Notification
from src.serializers.Notification.NotificationSerializer import NotificationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

class NotificationListView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def put(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_notification_by_parent_id(request, pk):
    parent_id = pk
    if not parent_id:
        return Response({'error': 'parent_id is required'}, status=status.HTTP_400_BAD_REQUEST)
   
    try:
        parent_id = uuid.UUID(parent_id)
    except ValueError:
        return Response({'error': 'parent_id must be a valid UUID'}, status=status.HTTP_400_BAD_REQUEST)


    notifications = Notification.objects.filter(parent_id=parent_id)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)    


@api_view(['GET'])
def change_all_is_read_to_true_by_parent_id(request, pk):
    parent_id=pk
    if not parent_id:
        return Response({'error': 'parent_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        parent_id = uuid.UUID(parent_id)
    except ValueError:
        return Response({'error': 'parent_id must be a valid UUID'}, status=status.HTTP_400_BAD_REQUEST)
    
    notifications = Notification.objects.filter(parent_id=parent_id)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    
    return Response({'message': 'All notifications have been marked as read'}, status=status.HTTP_200_OK)
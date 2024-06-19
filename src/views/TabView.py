
import json
import requests
import uuid
from rest_framework.views import APIView
from src.models import Driver
from src.serializers.History.TabSerializer import TabSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from src.serializers.History.HistorySerializer import HistorySerializer
from src.models.Parent import Parent
from src.models.UserKey import UserKey
from src.models.Child import Child
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from src.serializers.Notification.NotificationSerializer import NotificationSerializer
import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification

@api_view(['POST'])
def tab_view(request):
    serializer = TabSerializer(data=request.data)
    if serializer.is_valid():
        card_seri = serializer.validated_data.get('card_seri')
        type = serializer.validated_data.get('type')
        driver_id = serializer.validated_data.get('driver_id')
        
        location = serializer.validated_data.get('location')
        try:
            driver = Driver.objects.filter(id=driver_id).first()
            if driver.is_verify == False:
                return Response({"message": "Driver is not verify"}, status=400)
            response = create_history(card_seri, type, driver_id, location)
            if response.status_code == 200:
                response_noti = push_notification(response.data, driver_id)
                if response_noti.status_code == 200:
                    return Response(response.data, status=200)
                else:
                    return Response(response_noti.data, status=400)
            else:
                return Response(status=400)
        except ValueError as e:
            return Response({"message": str(e)}, status=400)
    else:
        return Response(serializer.errors, status=400)

def create_history(card_seri, type, driver_id, location):
    child = Child.objects.filter(card_number=card_seri).first()

    if child is None:
        return Response({"message": "thẻ chưa được liên kết"}, status=400)

    data = {
        'id': str(uuid.uuid4()),
        'type': type,
        'driver_id': driver_id,
        'child_id': child.id,
        'location': location
    }
    serializer = HistorySerializer(data=data)
    parent_id = child.parent_id

    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        data['parent_id'] = parent_id
        return Response(data, status=200)
    else:
        return Response(serializer.errors, status=400)


def push_notification(data, driver_id):
    configuration = onesignal.Configuration(
    app_key = "OTFmMTA5Y2YtYWNlNC00M2VlLWJlYmUtMjQyMDhhZDhkN2M3",
    user_key = "ZTQyYWNjMTItNGU0NC00ZTdhLWFhYzYtZDFjYWE3ODBlNjAw"
    )
    child_id = data["child_id"]
    parent_id = data["parent_id"]
    type = data["type"]
    parent = Parent.objects.filter(id=parent_id).first()
    
    list_device_key = UserKey.objects.filter(user_id=parent.id).all()
    child = Child.objects.filter(id=child_id).first()
    driver = Driver.objects.filter(id=driver_id).first()
    if driver.is_verify == False:
        return Response({"message": "Driver is not verify"}, status=400)
    # Create an API client with the configuration
    client = onesignal.ApiClient(configuration)
    api_instance = default_api.DefaultApi(client)
    
    if type == "in":
        heading =  {"en": f"{child.name} has arrived on the bus"}
        content =  {"en": f"{child.name} has arrived on the bus, driver: {driver.user_name}, bus number: {driver.bus_number}"}
    elif type == "out":
        heading =  {"en": f"{child.name} has departed from the bus"}
        content =  {"en": f"{child.name} has disembarked from the bus, driver: {driver.user_name}, bus number: {driver.bus_number}"}
    else:
        return Response({"message": "Invalid notification type"}, status=400)
    
    for device_key in list_device_key:
        try:
            notification = Notification(
                app_id="048155db-be80-4925-b5fd-4625451686f3",
                # include_player_ids=[device_key.key],
                include_player_ids=[device_key.key],
                headings=heading,
                contents=content,
            )
            
            api_response = api_instance.create_notification(notification)
            
            if api_response.id:
                noti_data={
                    "id": str(uuid.uuid4()),
                    "parent_id": parent_id,
                    "title": heading["en"],
                    "body": content["en"],
                }
                serializer = NotificationSerializer(data=noti_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)
            print(f"Notification sent: {api_response}")
        except onesignal.ApiException as e:
            return Response({"message": f"Exception when calling OneSignal API: {str(e)}"}, status=400)
    
    return Response({"message": "Notifications sent successfully"}, status=200)
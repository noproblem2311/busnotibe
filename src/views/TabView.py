
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
from src.models.Child import Child
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from src.serializers.Notification.NotificationSerializer import NotificationSerializer
@api_view(['POST'])
def tab_view(request):
    serializer = TabSerializer(data=request.data)
    if serializer.is_valid():
        card_seri = serializer.validated_data.get('card_seri')
        type = serializer.validated_data.get('type')
        driver_id = serializer.validated_data.get('driver_id')
        
        location = serializer.validated_data.get('location')
        print("tab_view_test: ", card_seri, type, driver_id, location)
        try:
            driver = Driver.objects.filter(id=driver_id).first()
            if driver.is_verify == False:
                return Response({"message": "Driver is not verify"}, status=400)
            response = create_history(card_seri, type, driver_id, location)
            if response.status_code == 200:
                response_noti = notification(response.data, driver_id)
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


def notification(data, driver_id):
    child_id = data["child_id"]
    parent_id = data["parent_id"]
    type = data["type"]
    parent = Parent.objects.filter(id=parent_id).first()
    
    device_ids = parent.device
    child = Child.objects.filter(id=child_id).first()
    driver = Driver.objects.filter(id=driver_id).first()
    if driver.is_verify == False:
        return Response({"message": "Driver is not verify"}, status=400)
    # Kiểm tra nếu device_ids là một chuỗi, chuyển đổi nó thành một list
    if isinstance(device_ids, str):
        device_ids = [device_ids]
        

    # Tạo thông báo dựa trên loại (type)
    if type == "in":
        notification_message = {
            "title": "Thông báo từ ứng dụng",
            "body": f"{child.name} bạn đã lên xe, tài xế: {driver.user_name}, số xe: {driver.bus_number}",
        }
    elif type == "out":
        notification_message = {
            "title": "Thông báo từ ứng dụng",
            "body": f"{child.name} đã xuống xe, tài xế {driver.user_name}, số xe: {driver.bus_number}",
        }
    else:
        return Response({"message": "Invalid notification type"}, status=400)

    # Gửi thông báo đến từng thiết bị
    for device_id in device_ids:
        try:
            # Tạo payload
            payload = {
                "to": device_id,
                "notification": notification_message
            }

            # Tạo headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": "key=AAAAw5nxWmM:APA91bG8DnxTg7wASeboLgi2GuQBjxaTzNsn1KDf9gKGopeWDTxx1dhMvsfr800GR3LCYJEtEFHU1eb_MD59aqqsEfh4dfqohmvcpboJeNOiQyfYkF3-d8kUGbE6LdUFOPGnxChciJAu"
            }

            # Gửi request
            response = requests.post("https://fcm.googleapis.com/fcm/send", json=payload, headers=headers)

            # Kiểm tra kết quả của request
            if response.status_code == 200:
                noti_data={
                    "id": str(uuid.uuid4()),
                    "parent_id": parent_id,
                    "title": notification_message["title"],
                    "body": notification_message["body"],
                }
                serializer = NotificationSerializer(data=noti_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)
                return Response({"message": "Đã gửi thông báo thành công"}, status=200)
            
            else:
                return Response({"message": f"Gửi thông báo thất bại, mã lỗi: {response.status_code}"}, status=response.status_code)
        except Exception as e:
            return Response({"message": str(e)}, status=400)

import uuid
from rest_framework.views import APIView
from src.serializers.History.TabSerializer import TabSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from src.serializers.History.HistorySerializer import HistorySerializer
from src.models.Parent import Parent
from src.models.Child import Child
@api_view(['POST'])
def tab_view(request):
    serializer = TabSerializer(data=request.data)
    if serializer.is_valid():
        card_seri = serializer.validated_data.get('card_seri')
        type= serializer.validated_data.get('type')
        driver_id = serializer.validated_data.get('driver_id')
        location = serializer.validated_data.get('location')
        response=create_history(card_seri,type, driver_id,location)
        if response.status_code == 200:
            response_noti=notification(response.data)
            if response_noti.status_code == 200:
                return Response(response.data, status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)
    else:
        return Response(serializer.errors, status=400)
    
def create_history(card_seri,type,driver_id,location):
    child = Child.objects.filter(card_number=card_seri).first()
   
    if child is None:
        return Response({"message": "thẻ chưa được liên kết"}, status=400)
    data={
        'id': str(uuid.uuid4()),
        'type': type,
        'driver_id': driver_id,
        'child_id': child.id,
        'location': location
    }
    serializer = HistorySerializer(data=data)
    parent_id=child.parent_id
    if serializer.is_valid():
        serializer.save()
        data=serializer.data
        data['parent_id']=parent_id
        return Response(data, status=200)
    else:
        return Response(serializer.errors, status=400)
def notification(data):
    driver_id=data["driver_id"]
    child_id=data["child_id"]
    parent_id=data["parent_id"]
    parent = Parent.objects.filter(id=parent_id).first()
    return Response({"driver_id":driver_id,"child_id":child_id,"parent_id":parent_id}, status=200)
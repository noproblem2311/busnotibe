from django.utils import timezone

from src.models.History import History
from src.models.Child import Child
from src.models.Driver import Driver
from src.serializers.History.HistorySerializer import HistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import timedelta 
from rest_framework import status

class HistoryListView(APIView):
    def get(self, request):
        histories = History.objects.all()
        serializer = HistorySerializer(histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return History.objects.get(pk=pk)
        except History.DoesNotExist:
            return None

    def get(self, request, pk):
        history = self.get_object(pk)
        if history is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HistorySerializer(history)
        return Response(serializer.data)

    def put(self, request, pk):
        history = self.get_object(pk)
        if history is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HistorySerializer(history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        history = self.get_object(pk)
        if history is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HistorySerializer(history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        history = self.get_object(pk)
        if history is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_tracking_by_parent_id(request, pk):
    parent_id = pk
    list_child_of_parent = Child.objects.filter(parent_id=parent_id)
    if not list_child_of_parent:
        return Response(status=status.HTTP_404_NOT_FOUND)

    history_by_child = []
    for child in list_child_of_parent:
        form_data = {
            "id":"",
            'child_id': "",
            "driver_avatar":"",
            "driver_name":"",
            "origin_position_name":"",
            "target_position_name":"",
            'child_name': "",
            'driver_id': "",
            "date": "",
            "bus_number": "",
            "get_on": {
                "time": "",
                "position":"",
                "message":""
                },
            "get_off": {"time": "",
                "position":"",
                "message":""},
            "tracking_id": ""
        }
        latest_histories = History.objects.filter(child_id=child.id).order_by('-created_at')[:2]
        form_data["child_id"] = child.id
        form_data["child_name"] = child.name
        if latest_histories:
            latest_history = latest_histories[0]
            form_data["driver_id"] = latest_history.driver_id
            form_data["date"] = latest_history.created_at
            driver = Driver.objects.filter(id=latest_history.driver_id).first()
            if driver:
                form_data["bus_number"] = driver.bus_number
                form_data["driver_name"] = driver.user_name
                form_data["driver_avatar"]= driver.avatar
                
            else:
                return Response({"error": f"No driver found for child {child.id}"}, status=status.HTTP_404_NOT_FOUND)
            form_data["tracking_id"] = latest_history.id
        if not latest_histories:
            pass
        elif len(latest_histories) == 1:
            latest_history = latest_histories[0]
            if latest_history.type == "in":
                form_data["get_on"] = {"time": latest_history.created_at, "position": latest_history.location}
                current_time = timezone.now()
                if current_time - latest_history.created_at > timedelta(minutes=600):
                    form_data["get_off"] = {"time":"", "position":"","message": "your child forgot to get off"}
                else:
                    form_data["get_off"] = {"time":"", "position":"","message": "on bus"}
            else:
                form_data["get_off"] = {"time": latest_history.created_at, "position": latest_history.location}
                form_data["get_on"] = {"message": "your child forgot to get on"}
        elif len(latest_histories) == 2:
            latest_history_1, latest_history_2 = latest_histories
            if latest_history_1.type == "in" and latest_history_2.type == "out":
                form_data["get_on"] = {"time": latest_history_1.created_at, "position": latest_history_1.location,"message":""}
                form_data["get_off"] = {"time": latest_history_2.created_at, "position": latest_history_2.location}
            elif latest_history_1.type == "out" and latest_history_2.type == "in":
                form_data["get_on"] = {"time": latest_history_2.created_at, "position": latest_history_2.location}
                current_time = timezone.now()  # Khởi tạo biến current_time
                if current_time - latest_history_2.created_at > timedelta(minutes=600):
                    form_data["get_off"] = {"message": "your child forgot to get off"}
                else:
                    form_data["get_off"] = {"message": "on bus"}
            elif latest_history_1.type == "in" and latest_history_2.type == "in":
                form_data["get_on"] = {"time": latest_history_2.created_at, "position": latest_history_2.location}
                current_time = timezone.now()  # Khởi tạo biến current_time
                if current_time - latest_history_1.created_at > timedelta(minutes=600):
                    form_data["get_off"] = {"message": "your child forgot to get off"}
                else:
                    form_data["get_off"] = {"message": "on bus"}
            elif latest_history_1.type == "out" and latest_history_2.type == "out":
                form_data["get_off"] = {"time": latest_history_2.created_at, "position": latest_history_2.location}
                form_data["get_on"] = {"message": "your child forgot to get on"}
        if form_data['driver_id'] !="":
            history_by_child.append(form_data)
    return Response(history_by_child)
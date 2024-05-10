from src.models.History import History
from src.serializers.History.HistorySerializer import HistorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
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



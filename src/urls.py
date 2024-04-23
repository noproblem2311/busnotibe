from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.ParentView import ParentListView, ParentDetailView
urlpatterns = [
    path('parents/', ParentListView.as_view(), name='parent-list'),
    path('parents/<str:pk>/', ParentDetailView.as_view(), name='parent-detail'),
]
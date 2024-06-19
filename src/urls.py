from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.ParentView import ParentListView, ParentDetailView, search_requests_parent
from .views.AuthView import login_view, signup_view, change_password_view, confirm_otp
from .views.DriverView import DriverListView, DriverDetailView, search_requests_driver
from .views.RequestView import RequestListView, RequestDetailView
from .views.TemplateView import TemplateListView, TemplateDetailView, search_requests_template
from .views.ChildView import ChildListView, ChildDetailView
from .views.AuthView import forgot_password_view, confirm_forgot_password_view, resend_confirmation_code
from .views.HistoryView import HistoryListView, HistoryDetailView,list_tracking_by_parent_id
from .views.TabView import tab_view
from .views.ChildView import list_child_by_parent_id
from .views.SchoolView import SchoolDetailView,SchoolListView,search_requests_school
from .views.RequestView import list_request_by_parent_id, search_requests
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from .views.AdminView import AdminListView, AdminDetailView
from .views.CompanyView import CompanyListView, CompanyDetailView, search_requests_company
from .views.NotificationView import NotificationListView,  NotificationDetailView, list_notification_by_parent_id, change_all_is_read_to_true_by_parent_id
from .views.UserKeyView import  UserKeyDetailView,UserKeyView, delete_by_key
urlpatterns = [
    path('api_schema', get_schema_view(title="Busnotibe API",url='/dev/'), name="api_schema"),
    path('swagger-ui/',TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'api_schema'}  
    ), name='swagger-ui'),
    path('parents/', ParentListView.as_view(), name='parent-list'),
    path('parents/search/', search_requests_parent, name='parent-search'),
    path('parents/<str:pk>/', ParentDetailView.as_view(), name='parent-detail'),
    
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/search/', search_requests_driver, name='driver-search'),
    path('drivers/<str:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('changepassword/', change_password_view, name='changepassword'),
    path('confirmotp/', confirm_otp, name='confirmotp'),
    
    path('requests/', RequestListView.as_view(), name='request-list'),
    path('requests/search/', search_requests, name='request-search'),
    path('requests/<str:pk>/', RequestDetailView.as_view(), name='request-detail'),
    
    path('templates/', TemplateListView.as_view(), name='template-list'),
    path('templates/search/', search_requests_template, name='template-search'),
    path('templates/<str:pk>/', TemplateDetailView.as_view(), name='template-detail'),
    
    path('children/', ChildListView.as_view(), name='child-list'),
    path('children/<str:pk>/', ChildDetailView.as_view(), name='child-detail'),
    
    path('forgotpassword/', forgot_password_view, name='forgot_password'),
    path('confirmforgotpassword/', confirm_forgot_password_view, name='confirm_forgot_password'),
    
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('history/<str:pk>/', HistoryDetailView.as_view(), name='history-detail'),
    
    path('tab/', tab_view, name='tab'),
    
    path('listchild/<str:pk>/', list_child_by_parent_id, name='list_child_by_parent_id'),
    path('listrequest/<str:pk>/', list_request_by_parent_id, name='list_request_by_parent_id'),
    
    path('schools/', SchoolListView.as_view(), name='school-list'),
    path('schools/search/', search_requests_school, name='school-search'),
    path('schools/<str:pk>/', SchoolDetailView.as_view(), name='school-detail'),
    
    path('resendconfirmationcode/', resend_confirmation_code, name='resend_confirmation_code'),
    path('listtracking/<str:pk>/', list_tracking_by_parent_id, name='list_tracking_by_parent_id'),
    
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('admins/<str:pk>/', AdminDetailView.as_view(), name='admin-detail'),
    
    path('company/', CompanyListView.as_view(), name='company-list'),
    path('company/search/', search_requests_company, name='company-search'),
    path('company/<str:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    
    path('notification/', NotificationListView.as_view(), name='notification-list'),
    path('notification/<str:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notification/list/<str:pk>/', list_notification_by_parent_id, name='list_notification_by_parent_id'),
    path('notification/read-all/<str:pk>/', change_all_is_read_to_true_by_parent_id, name='change_all_is_read_to_true_by_parent_id'),
    
    path('userkey/', UserKeyView.as_view(), name='userkey-list'),
    path('userkey/delete/<str:pk>/', delete_by_key, name='delete_by_key'),
    path('userkey/<str:pk>/', UserKeyDetailView.as_view(), name='userkey-detail'),

]

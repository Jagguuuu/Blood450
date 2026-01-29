from django.urls import path
from . import views

urlpatterns = [
    # Home redirect
    path('home/', views.home_redirect, name='home_redirect'),
    
    # Admin pages
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-request/', views.admin_create_request, name='admin_create_request'),
    path('request/<int:request_id>/', views.admin_request_detail, name='admin_request_detail'),
    
    # Donor pages
    path('notifications/', views.donor_notifications, name='donor_notifications'),
    
    # API endpoints
    path('respond/', views.donor_respond, name='donor_respond'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.agency_login, name='agency_login'),
    path('dashboard/', views.agency_dashboard, name='agency_dashboard'),
    path('', views.home, name='home'),
    path('agency/dashboard/', views.agency_dashboard, name='agency_dashboard'),
    path('complaints/respond/<int:complaint_id>/', views.respond_to_complaint, name='respond_to_complaint'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    # path('login/', auth_views.LoginView.as_view(template_name='complaints/login.html'), name='login'),
    path('status/<int:complaint_id>/', views.complaint_status, name='complaint_status'),
    path('respond/<int:complaint_id>/', views.respond_to_complaint, name='respond_to_complaint'),
]

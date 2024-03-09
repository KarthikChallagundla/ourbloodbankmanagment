"""bloodbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blood import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('donor/', include('donor.urls')),
    path('patient/', include('patient.urls')),

    path('', views.home_view, name='home'),
    path('logout', LogoutView.as_view(template_name='blood/logout.html'),name='logout'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin/', LoginView.as_view(template_name='blood/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-blood/', views.admin_blood_view, name='admin-blood'),
    path('admin-donor/', views.admin_donor_view, name='admin-donor'),
    path('update-donor/<int:id>', views.update_donor_view, name='update-donor'),
    path('delete-donor/<int:id>', views.delete_donor_view,name='delete-donor'),
    path('admin-patient/', views.admin_patient_view, name='admin-patient'),
    path('update-patient/<int:id>', views.update_patient_view, name='update-patient'),
    path('delete-patient/<int:id>', views.delete_patient_view, name='delete-patient'),
    path('admin-donation/', views.admin_donation_view, name='admin-donation'),
    path('approve-donation/<int:id>', views.approve_donation_view, name='approve-donation'),
    path('reject-donation/<int:id>', views.reject_donation_view, name='reject-donation'),
]

from django.urls import path
from . import views
urlpatterns = [
    path('patientlogin/', views.patientlogin, name='patientlogin')
]
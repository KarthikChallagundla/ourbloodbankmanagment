from django.urls import path
from . import views
urlpatterns = [
    path('donorlogin/', views.donorlogin, name="donorlogin"),
]
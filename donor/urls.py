from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('donorlogin/', LoginView.as_view(template_name='donor/donorlogin.html'), name="donorlogin"),
    path('donorsignup/', views.donor_signup_view, name="donorsignup"),
]
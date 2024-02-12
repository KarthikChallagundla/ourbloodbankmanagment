from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def home_view(request):
    return render(request, 'blood/index.html')

def admin_login(request):
    return render(request, 'blood/adminlogin.html')
from django.shortcuts import render

# Create your views here.

def donorlogin(request):
    return render(request, 'donor/donorlogin.html')
from django.shortcuts import render

# Create your views here.

def patientlogin(request):
    return render(request, 'patient/patientlogin.html')
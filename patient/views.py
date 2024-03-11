from django.shortcuts import render
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from blood import models as bmodels
from blood import forms as bforms

# Create your views here.

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.first_name = userForm.cleaned_data['first_name']
            user.last_name = userForm.cleaned_data['last_name']
            user.username = userForm.cleaned_data['username']
            user.password = userForm.cleaned_data['password']
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.age = patientForm.cleaned_data['age']
            patient.disease = patientForm.cleaned_data['disease']
            patient.address = patientForm.cleaned_data['address']
            patient.doctorname = patientForm.cleaned_data['doctorname']
            patient.mobile = patientForm.cleaned_data['mobile']
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('../patientlogin')
    return render(request, 'patient/patientsignup.html', context=mydict)

def patient_dashboard_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),
    }
    return render(request,'patient/patient_dashboard.html',context=dict)

def make_request_view(request):
    request_form = bforms.RequestForm()
    mydict={'request_form' : request_form}
    if request.method == 'POST': 
        request_form = bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient=models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('../my-request')
    return render(request,'patient/makerequest.html', context=mydict)

def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})

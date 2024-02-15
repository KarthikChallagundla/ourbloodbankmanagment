from django.shortcuts import render
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

# Create your views here.

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST)
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
        return HttpResponseRedirect('patientlogin')
    return render(request, 'patient/patientsignup.html', context=mydict)

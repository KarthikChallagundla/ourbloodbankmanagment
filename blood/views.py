from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms, models
from donor import models as dmodels
from donor import forms as dforms
from patient import models as pmodels
from patient import forms as pforms

# Create your views here.

def home_view(request):
    x = models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()
        if request.user.is_authenticated:
            return HttpResponseRedirect('afterlogin')
    return render(request, 'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor/donor-dashboard')           
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        return redirect('admin-dashboard')
    
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict = {
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count(),
    }
    return render(request, 'blood/admin_dashboard.html', context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict = {
        'bloodForm' : forms.BloodForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm = forms.BloodForm(request.POST)
        if bloodForm.is_valid():
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('../admin-blood')
    return render(request, 'blood/admin_blood.html', context=dict)

@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request, 'blood/admin_donor.html', {'donors':donors})

@login_required(login_url='adminlogin')
def update_donor_view(request, id):
    donor=dmodels.Donor.objects.get(id=id)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm, 'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request, 'blood/update_donor.html', context=mydict)

@login_required(login_url='adminlogin')
def delete_donor_view(request,id):
    donor=dmodels.Donor.objects.get(id=id)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request, 'blood/admin_patient.html', {'patients' : patients})

@login_required(login_url='adminlogin')
def update_patient_view(request, id):
    patient=pmodels.Patient.objects.get(id=id)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES, instance=patient)
    dict={'userForm':userForm, 'patientForm':patientForm}
    if userForm.is_valid() and patientForm.is_valid():
        user=userForm.save()
        user.setpassword(user.password)
        user.save()
        patient=patientForm.save(commit=False)
        patient.user=user
        patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
        patient.save()
        return HttpResponseRedirect('admin-patient')
    return render(request, 'blood/update_patient.html', context=dict)

@login_required(login_url='adminlogin')
def delete_patient_view(request, id):
    patient=pmodels.Patient.objects.get(id=id)
    user=pmodels.User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.all()
    return render(request, 'blood/admin_donation.html', {'donations':donations})

@login_required(login_url='adminlogin')
def approve_donation_view(request, id):
    donation=dmodels.BloodDonate.objects.get(id=id)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    return HttpResponseRedirect('../admin-donation')

@login_required(login_url='adminlogin')
def reject_donation_view(request, id):
    donation=dmodels.BloodDonate.objects.get(id=id)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('../admin-donation')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'blood/admin_request.html', {'requests':requests})

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request, 'blood/admin_request_history.html', {'requests':requests})

@login_required(login_url='adminlogin')
def update_approve_status_view(request, id):
    req=models.BloodRequest.objects.get(id=id)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit = stock.unit - unit
        stock.save()
        req.status="Approved"
    else:
        message="Stock doesnot have enough blood only " + str(stock.unit) + " units are available"
    req.save()

    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request, 'blood/admin_request.html', {'requests':requests , 'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request, id):
    req=models.BloodRequest.objects.get(id=id)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')
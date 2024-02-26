from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from . import forms, models
from blood import models as bmodels
from blood import forms as bforms
# Create your views here.

def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm, 'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST)
        if userForm.is_valid() and donorForm.is_valid():
            user = userForm.save()
            user.first_name = userForm.cleaned_data['first_name']
            user.last_name = userForm.cleaned_data['last_name']
            user.username = userForm.cleaned_data['username']
            user.password = userForm.cleaned_data['password']
            user.set_password(user.password)
            user.save()
            donor = donorForm.save(commit=False)
            donor.user = user
            donor.address = donorForm.cleaned_data['address']
            donor.mobile = donorForm.cleaned_data['mobile']
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('../donorlogin')
    return render(request, 'donor/donorsignup.html', context=mydict)

def donor_dashboard_view(request):
    donor = models.Donor.objects.get(user_id=request.user.id)
    dict = {
        'requestpending' : bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved' : bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade' : bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected' : bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


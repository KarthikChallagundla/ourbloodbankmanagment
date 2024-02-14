from django import forms

from . import models

class BloodForm(forms.ModelForm):
    class Meta:
        models=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        models=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']
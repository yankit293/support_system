from django import forms
from .models import RaiseRequest, Issue
from phonenumber_field.modelfields import PhoneNumberField

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = RaiseRequest
        fields = ['name','email','phone_number','description','issue','image']

        widgets = {'description':forms.Textarea(attrs={'rows': 3})
        }

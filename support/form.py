from django import forms
from .models import RaiseRequest, Issue

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = RaiseRequest
        fields = ['name', 'email', 'description', 'issue', 'image']

        widgets = {'description':forms.Textarea}
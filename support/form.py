from django import forms
from .models import RaiseRequest, Issue, ReportUser
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget,PhoneNumberPrefixWidget,PhonePrefixSelect,TextInput

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = RaiseRequest
        fields = ['name','email','phone_number','description','issue','image']

        widgets = {'description':forms.Textarea(attrs={'rows': 3}),
                    'phone_number':PhoneNumberPrefixWidget(attrs={'class':'form-control col-md-4 mb-0'})
        }

class ReportForm(forms.ModelForm):

    class Meta:
        model = ReportUser
        
        fields = ['name','email','subject','description','image']

        widgets = {'description':forms.Textarea(attrs={'rows':3,
                                                        'placeholder':"Please provide as much detail as possible about the accountor behavior you are reporting. It's especially helpful to include specific examples in the form of URLs or screenshots."
                                                        })}
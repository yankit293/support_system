from django import forms
from .models import RaiseRequest, Issue, ReportUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget,PhoneNumberPrefixWidget,PhonePrefixSelect,TextInput
from intl_tel_input.widgets import IntlTelInputWidget

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = RaiseRequest
        fields = ['name','email','phone_number','description','issue','image']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "unique",
            }
        }

        widgets = {'description':forms.Textarea(attrs={'rows': 3, 'placeholder':'Let us know. What problem are you facing at Piblitz?'}),
                    'phone_number':IntlTelInputWidget(attrs={'style':'width=100%;'},default_code='IN')
        }

class ReportForm(forms.ModelForm):

    class Meta:
        model = ReportUser
        
        fields = ['name','email','subject','description','image']

        widgets = {'description':forms.Textarea(attrs={'rows':3,
                                                        'placeholder':"Please provide as much detail as possible about the accountor behavior you are reporting. It's especially helpful to include specific examples in the form of URLs or screenshots."
                                                        })}

class StatusForm(forms.Form):
    choices = (
        ('1', 'Payment processing failure'),
        ('2', 'Refund')
    )
    email = forms.EmailField()
    issue = forms.ChoiceField(choices=choices)
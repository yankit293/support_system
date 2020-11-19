from django import forms
from .models import RaiseRequest, Issue
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget,PhoneNumberPrefixWidget,PhonePrefixSelect,TextInput
from intl_tel_input.widgets import IntlTelInputWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


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

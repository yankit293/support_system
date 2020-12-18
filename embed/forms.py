from django import forms

class urlInputForm(forms.Form):
    url = forms.URLField(max_length=300)
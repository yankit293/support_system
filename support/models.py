from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from .validator import file_size

class Issue(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title
name_regex = RegexValidator(regex=r'^[a-zA-Z ]+$', message="Only enter alphabet!")
class RaiseRequest(models.Model):
    name = models.CharField(max_length=30, validators=[name_regex])
    email = models.EmailField(max_length=100,help_text='Optional')
    phone_number = PhoneNumberField()
    description = models.CharField(max_length=400,help_text='Describ your issue here.', validators=[MinLengthValidator(30)])
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    image = models.ImageField(validators=[file_size], help_text='Size should not exceed 5 MiB.')
    date = models.DateTimeField(auto_now_add=True)

class ReportUser(models.Model):
    name = models.CharField(max_length=30, validators=[name_regex])
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=50)
    description = models.CharField(max_length=400,help_text='Describ your issue here.')
    image = models.ImageField(validators=[file_size], help_text='Size should not exceed 5 MiB.')

    
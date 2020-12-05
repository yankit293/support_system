from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from .validator import file_size
from django.contrib.auth.models import User

class Issue(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class Status(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title

class Reason(models.Model):
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title
name_regex = RegexValidator(regex=r'^[a-zA-Z ]+$', message="Only enter alphabet!")
#model of RaiseRequest.
class RaiseRequest(models.Model):
    name = models.CharField(max_length=30, validators=[name_regex])
    email = models.EmailField(max_length=100,help_text='Optional')
    phone_number = PhoneNumberField()
    description = models.CharField(max_length=400, validators=[MinLengthValidator(30)])
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    image = models.ImageField(validators=[file_size], help_text='Size should not exceed 5 MiB.')
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'payment-issue'
        unique_together = ['email','issue']

class ReportUser(models.Model):
    name = models.CharField(max_length=30, validators=[name_regex])
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=50)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    description = models.CharField(max_length=400)
    image = models.ImageField(validators=[file_size], help_text='Size should not exceed 5 MiB.')
    class Meta:
        db_table = "report_user"
        unique_together = ['email','username','reason']

class ReportContent(models.Model):
    name = models.CharField(max_length=30, validators=[name_regex])
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=50)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    description = models.CharField(max_length=400)
    status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    image = models.ImageField(validators=[file_size], help_text='Size should not exceed 5 MiB.')
    url = models.URLField(max_length=200)
    class Meta:
        db_table = "report_content"
        unique_together = ['email','subject','reason']

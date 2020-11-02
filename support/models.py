from django.db import models
from django.core.exceptions import ValidationError

class Issue(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class RaiseRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField( max_length=100)
    description = models.CharField(max_length=400)
    image = models.ImageField() 
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

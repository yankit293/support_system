from django.db import models


class Router(models.Model):
    specifications = models.FileField(upload_to='router_specifications')
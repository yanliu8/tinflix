from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tinflixer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #add custom features here


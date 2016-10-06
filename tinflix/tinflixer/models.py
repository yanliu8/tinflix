from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tinflixer(models.Model):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #add custom features here
    gender = models.CharField(max_length=20, null=True, blank=True,
                              choices=GENDERS)


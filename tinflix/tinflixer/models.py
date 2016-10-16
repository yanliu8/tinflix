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
    low_age = models.IntegerField(blank=True, null=True)
    high_age = models.IntegerField(blank=True, null=True)
    real_age = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    longtitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)  # test empty facebook profile pic
    about_me = models.TextField(blank=True, null=True)
    sex_orin = models.CharField(max_length=20, null=True, blank=True, choices=GENDERS)


class Liked_Movie(models.Model):
    user = models.ForeignKey('Tinflixer', related_name='%(app_label)s_%(class)s_user')
    movie = models.ForeignKey('movie.Movie', related_name='%(app_label)s_%(class)s_movie')


class Liked_User(models.Model):
    user1 = models.ForeignKey('Tinflixer', related_name='%(app_label)s_%(class)s_user1')
    user2 = models.ForeignKey('Tinflixer', related_name='%(app_label)s_%(class)s_user2')
    movie = models.ForeignKey('movie.Movie', related_name='%(app_label)s_%(class)s_movie')

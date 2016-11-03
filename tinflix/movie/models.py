from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80, blank=True, null=True)
    release_date = models.TextField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)
    cast_crew = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)

class Similar(models.Model):
    movie_1 = models.ForeignKey('Movie', related_name='%(app_label)s_%(class)s_movie1')
    movie_2 = models.ForeignKey('Movie', related_name='%(app_label)s_%(class)s_movie2')

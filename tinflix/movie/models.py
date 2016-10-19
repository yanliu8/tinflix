from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    year = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    genre = models.CharField(max_length=10, blank=True, null=True)
    cast_crew = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


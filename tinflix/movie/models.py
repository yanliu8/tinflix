from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    release_date = models.TextField(blank=True, null=True)
    rating = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)
    cast_crew = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)

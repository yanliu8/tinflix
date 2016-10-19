from django.contrib import admin
from movie.models import Movie

# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_id']


admin.site.register(Movie, MovieAdmin)

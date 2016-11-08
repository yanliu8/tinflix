from django.contrib import admin
from tinflixer.models import *
# Register your models here.
class TinflixerAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'gender',
                    'low_age',
                    'high_age',
                    'real_age',
                    'city',
                    'state',
                    'picture',
                    'about_me',
                    ]


class Liked_MovieAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'movie']


admin.site.register(Tinflixer, TinflixerAdmin)
admin.site.register(Liked_Movie, Liked_MovieAdmin)

from django.contrib import admin
from tinflixer.models import Tinflixer
# Register your models here.
class TinflixerAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'gender',
                    'low_age',
                    'high_age',
                    'real_age',
                    'longtitude',
                    'latitude',
                    'picture',
                    'about_me',
                    'sex_orin']


admin.site.register(Tinflixer, TinflixerAdmin)


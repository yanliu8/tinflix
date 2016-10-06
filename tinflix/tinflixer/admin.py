from django.contrib import admin
from tinflixer.models import Tinflixer
# Register your models here.
class TinflixerAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'gender']


admin.site.register(Tinflixer, TinflixerAdmin)


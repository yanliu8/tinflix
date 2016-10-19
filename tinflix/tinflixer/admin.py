from django.contrib import admin
from tinflixer.models import Tinflixer
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


admin.site.register(Tinflixer, TinflixerAdmin)


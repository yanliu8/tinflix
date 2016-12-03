"""tinflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import tinflixer.views
import movie.views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
urlpatterns = [
               url(r'', include('social.apps.django_app.urls', namespace='social')),
               url(r'', include('django.contrib.auth.urls', namespace='auth')),
               url(r'^$', tinflixer.views.index),
               url('^admin/', include(admin.site.urls)),
    url('^signup$', tinflixer.views.signup),
    url('^stage4$', movie.views.stage4),
    url('^movies$', movie.views.index),
    url('^movie/ajax/like$', movie.views.like_by_search),
    url('^user/ajax/like$', movie.views.like_user),
    url('^movie/search', movie.views.search),
    url('profile', tinflixer.views.profile),
    # url('^detail', movie.views.detail),
    url('^like_history', movie.views.like_history),
    url('^user_recommendation/', movie.views.user_liked_same_movie)
               ]
urlpatterns += staticfiles_urlpatterns()

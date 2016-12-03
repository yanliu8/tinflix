from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from django.db.models import Q
from tinflixer.models import *
from django.contrib.auth.decorators import login_required
import googlemaps


# Create your views here.

def index(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})
    if not request.user or not request.user.is_authenticated():
        return render_to_response("mainpage.html", context)
    obj = Tinflixer.objects.get(user=request.user)
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'tinflixer': obj})
    if obj.new:
        obj.new = False
        obj.save()
        return redirect("/signup", tinflixer=obj)
    return render_to_response("mainpage.html", context)


@login_required
def signup(request):
    if request.method == 'POST':
        tinflixer_obj = Tinflixer.objects.get(user=request.user)
        tinflixer_obj.city = request.POST.get('city')
        tinflixer_obj.first_name = request.POST.get('first_name')
        tinflixer_obj.last_name = request.POST.get('last_name')
        tinflixer_obj.state = request.POST.get('state')
        tinflixer_obj.real_age = request.POST.get('age')
        tinflixer_obj.email = request.POST.get('email')
        tinflixer_obj.gender = request.POST.get('gender')
        tinflixer_obj.about_me = request.POST.get('about_me')
        tinflixer_obj.address = request.POST.get('address')
        gmaps = googlemaps.Client(key="AIzaSyC2djR2E8beAWvvaIG49zuiWftsJqDKJNQ")
        geocode_result = gmaps.geocode(tinflixer_obj.address)
        tinflixer_obj.latitude = geocode_result[0]['geometry']['location']['lat']
        tinflixer_obj.longtitude = geocode_result[0]['geometry']['location']['lng']
        tinflixer_obj.save()
        return redirect("/")
    obj = Tinflixer.objects.get(user=request.user)
    return render(request, "signup.html", {'tinflixer': obj})


@login_required
def profile(request):
    if request.method == 'POST':
        tinflixer_obj = Tinflixer.objects.get(user=request.user)
        tinflixer_obj.first_name = request.POST.get('first_name')
        tinflixer_obj.last_name = request.POST.get('last_name')
        tinflixer_obj.city = request.POST.get('city')
        tinflixer_obj.state = request.POST.get('state')
        tinflixer_obj.real_age = request.POST.get('age')
        tinflixer_obj.email = request.POST.get('email')
        tinflixer_obj.gender = request.POST.get('gender')
        tinflixer_obj.about_me = request.POST.get('about_me')
        if tinflixer_obj.address != request.POST.get('address'):
            tinflixer_obj.address = request.POST.get('address')
            gmaps = googlemaps.Client(key="AIzaSyC2djR2E8beAWvvaIG49zuiWftsJqDKJNQ")
            geocode_result = gmaps.geocode(tinflixer_obj.address)
            tinflixer_obj.latitude = geocode_result[0]['geometry']['location']['lat']
            tinflixer_obj.longtitude = geocode_result[0]['geometry']['location']['lng']
        tinflixer_obj.save()
        return redirect("/profile")
    tinflixer = Tinflixer.objects.get(user=request.user)
    relationships = []
    liked_user = Liked_User.objects.filter(Q(user1=tinflixer) | Q(user2=tinflixer))
    for l in liked_user:
        if l.user1 == tinflixer:
            relationships.append({"user": l.user2, "relation": l.status})
        else:
            relationships.append({"user": l.user1, "relation": l.status})
    return render(request, "members.html", {'tinflixer': tinflixer, "users": relationships})


@login_required
def liked_user(request):
    user = Tinflixer.objects.get(user=request.user)
    liked = Liked_User.objects.filter(Q(user1=user) | Q(user2_2=user))
    return render(request, "like_user.html", {'liked': liked})

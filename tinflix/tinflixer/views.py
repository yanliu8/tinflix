from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from django.db.models import Q
from tinflixer.models import *
from django.contrib.auth.decorators import login_required


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
        # tinflixer_obj.email = request.POST.get('email')
        tinflixer_obj.gender = request.POST.get('gender')
        # tinflixer_obj.about_me = request.POST.get('about_me')
        print tinflixer_obj.real_age
        tinflixer_obj.save()
        return redirect("/profile")
    obj = Tinflixer.objects.get(user=request.user)
    return render(request, "members.html", {'tinflixer': obj})


@login_required
def liked_user(request):
    user = Tinflixer.objects.get(user=request.user)
    liked = Liked_User.objects.filter(Q(user1=user) | Q(user2_2=user))
    return render(request, "like_user.html", {'liked': liked})

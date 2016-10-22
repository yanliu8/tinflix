from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from tinflixer.models import Tinflixer
# Create your views here.

def index(request):
    context = RequestContext(request,
                             {'request' : request,
                              'user' : request.user})
    if not request.user or not request.user.is_authenticated():
        return render_to_response("mainpage.html", context)
    obj = Tinflixer.objects.get(user=request.user)
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'tinflixer': obj})
    if obj.new:
        # request.user.new = False

        return redirect("/signup/", tinflixer=obj)
    return render_to_response("mainpage.html", context)


def signup(request):
    if request.method == 'POST':
        tinflixer_obj = Tinflixer.objects.get(user=request.user)
        tinflixer_obj.city = request.POST.get('city')
        tinflixer_obj.state = request.POST.get('state')
        tinflixer_obj.real_age = request.POST.get('age')
        tinflixer_obj.email = request.POST.get('email')
        tinflixer_obj.gender = request.POST.get('gender')
        tinflixer_obj.about_me = request.POST.get('about_me')
        tinflixer_obj.save()
        return redirect("/")
    obj = Tinflixer.objects.get(user=request.user)
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'tinflixer': obj})
    return render(request, "test_signup.html", context)

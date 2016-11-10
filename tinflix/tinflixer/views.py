from django.shortcuts import render_to_response, redirect, render
from django.template.context import RequestContext
from tinflixer.models import Tinflixer
from tinflixer.models import Liked_Movie
from movie.models import Similar
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from movie.models import Movie
import omdb
import requests


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
        # tinflixer_obj.city = request.POST.get('city')
        # tinflixer_obj.state = request.POST.get('state')
        tinflixer_obj.real_age = request.POST.get('age')
        # tinflixer_obj.email = request.POST.get('email')
        # tinflixer_obj.gender = request.POST.get('gender')
        # tinflixer_obj.about_me = request.POST.get('about_me')
        tinflixer_obj.save()
        return redirect("/profile")
    obj = Tinflixer.objects.get(user=request.user)
    return render(request, "members.html", {'tinflixer': obj})


def recommendation(request):
    user = request.user
    liked = Liked_Movie.objects.filter(user=user).order_by('-id')
    liked = liked[:2]
    recommendations = []
    for liked_obj in liked:
        movie = liked_obj.movie
        similar = Similar.objects.filter(Q(movie_1=movie) | Q(movie_2=movie))
        if len(similar) == 0:
            params = {"q": movie.name, "type": "movie", "k": "240885-tinflixe-OOASJ4XK"}
            try:
                r = requests.get("https://www.tastekid.com/api/similar", params=params).json()
            except:
                continue
            lst = r['Similar']['Results']
            for obj in lst:
                name = obj['Name']
                try:
                    movie_obj = Movie.objects.get(name=name)
                except Movie.DoesNotExist:
                    api_result = omdb.title(name)
                    if api_result:
                        movie_obj = Movie(name=name)
                        movie_obj.plot = api_result['plot'].encode('utf-8')
                        movie_obj.duration = api_result['runtime'].encode('utf-8')
                        movie_obj.release_date = api_result['released'].encode('utf-8')
                        movie_obj.rating = api_result['imdb_rating'].encode('utf-8')
                        movie_obj.poster = api_result['poster'].encode('utf-8')
                        movie_obj.cast_crew = api_result['actors'].encode('utf-8')
                        movie_obj.genre = api_result['genre'].encode('utf-8')
                        movie_obj.save()
                    else:
                        continue
                new_similar = Similar(movie_1=movie, movie_2=movie_obj)
                new_similar.save()
            similar = Similar.objects.filter(movie_1=movie)
        if len(similar) > 10:
            similar = similar[:5]
        for i in similar:
            recommendations.append(i)

    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'recommendations': recommendations})
    return render(request, "recommendations.html", context)

from __future__ import print_function
from django.shortcuts import render
from tinflixer.models import *
from django.db.models import Q
import requests
from django_ajax.decorators import ajax
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from movie.models import *
import omdb
# Create your views here.


def stage4(request):
    movie = Movie.objects.get(name='The Jungle Book')
    context = RequestContext(request,
                             {'request': request,
                              'movie': movie})
    return render(request, 'stage4.html', context)


def get_movie_detail(movie_obj):
    name = movie_obj.name
    api_result = omdb.title(name)
    if not api_result:
        return None
    movie_obj.plot = api_result['plot'].encode('utf-8')
    movie_obj.duration = api_result['runtime'].encode('utf-8')
    movie_obj.release_date = api_result['released'].encode('utf-8')
    movie_obj.rating = api_result['imdb_rating'].encode('utf-8')
    movie_obj.poster = api_result['poster'].encode('utf-8')
    movie_obj.cast_crew = api_result['actors'].encode('utf-8')
    movie_obj.genre = api_result['genre'].encode('utf-8')
    movie_obj.save()
    return movie_obj


@login_required
def search(request):
    if request.method == 'GET':
        name = request.GET.get('q')
        if not name:
            raise Http404
        result = Movie.objects.filter(name__icontains=name).order_by('-rating')
        if not result.exists():
            movie_obj = Movie(name=name)
            ret = get_movie_detail(movie_obj)
            if not ret:
                result = None
            else:
                result = [ret]
        updated = False
        if not result:
            return render(request, "search.html", {'movies': None})
        for obj in result:
            if obj.rating == "N/A":
                obj.rating = "0.0"
                obj.save()
                updated = True
            if obj.poster == "N/A":
                obj.poster = None
                obj.save()
                updated = True
        if updated:
            result = Movie.objects.filter(name__icontains=name).order_by('-rating')
        movies = []
        for movie_obj in result:
            tinflixer = Tinflixer.objects.get(user=request.user)
            if Liked_Movie.objects.filter(movie=movie_obj).filter(user=tinflixer).exists():
                movies.append({"movie": movie_obj, "like": True})
            else:
                movies.append({"movie": movie_obj, "like": False})
        return render(request, 'search.html', {'movies': movies})


@ajax
@csrf_exempt
@login_required
def like_by_search(request):
    movie = Movie.objects.get(movie_id=request.POST['movie'])
    user = Tinflixer.objects.get(user=request.user)
    if Liked_Movie.objects.filter(user=user).filter(movie=movie).exists():
        old_like = Liked_Movie.objects.get(user=user, movie=movie)
        old_like.delete()
    else:
        new_like = Liked_Movie(user=user, movie=movie)
        new_like.save()


@login_required
def like_history(request):
    tinflixer = Tinflixer.objects.get(user=request.user)
    result = Liked_Movie.objects.filter(user=tinflixer)
    movies = []
    for like in result:
        movies.append({"movie": like.movie, "like": True})
    return render(request, 'search.html', {'movies': movies})


def index(request):
    user = Tinflixer.objects.get(user=request.user)
    liked = Liked_Movie.objects.filter(user=user).order_by('-id')
    recommendations = []
    for liked_obj in liked:
        movie = liked_obj.movie
        similar = Similar.objects.filter(Q(movie_1=movie) | Q(movie_2=movie))
        if not similar.exists():
            params = {"q": movie.name, "type": "movie", "k": "240885-tinflixe-BDIBVZFX"}
            try:
                r = requests.get("https://www.tastekid.com/api/similar", params=params).json()
            except:
                continue
            print(r)
            lst = r['Similar']['Results']
            for obj in lst:
                name = obj['Name']
                try:
                    movie_obj = Movie.objects.get(name=name)
                except Movie.DoesNotExist:
                    api_result = omdb.title(name)
                    if api_result:
                        movie_obj = Movie(name=name)
                        movie_obj = get_movie_detail(movie_obj)
                    else:
                        continue
                new_similar = Similar(movie_1=movie, movie_2=movie_obj)
                new_similar.save()
        similar = Similar.objects.filter(Q(movie_1=movie) | Q(movie_2=movie))
        for obj in similar:
            if obj.movie_1.movie_id == movie.movie_id:
                if not obj.movie_2.rating:
                    recommendations.append(get_movie_detail(obj.movie_2))
                elif obj.movie_2.poster == 'N/A':
                    obj.movie_2.poster = None
                    recommendations.append(obj.movie_2)
                else:
                    recommendations.append(obj.movie_2)
            else:
                if not obj.movie_1.rating:
                    recommendations.append(get_movie_detail(obj.movie_1))
                elif obj.movie_1.poster == 'N/A':
                    obj.movie_1.poster = None
                    recommendations.append(obj.movie_1)
                else:
                    recommendations.append(obj.movie_1)
        if len(recommendations) >= 10:
            break
    recommendations = recommendations[:10]
    return render(request, "moviePage.html", {'request': request,
                                              'user': request.user,
                                              'recommendations': recommendations})

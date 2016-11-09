from __future__ import print_function
from django.shortcuts import render
from tinflixer.models import *
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


def get_movie_detail(name, movie_obj):
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
    votes = api_result['imdb_votes'].encode('utf-8').replace(',', '')
    if votes == 'N/A':
        movie_obj.popularity = 0
    else:
        movie_obj.popularity = int(votes)
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
            ret = get_movie_detail(name, movie_obj)
            if not ret:
                movie_obj.delete()
                result = None
            else:
                result = [ret]
        updated = False
        for obj in result:
            print(obj.rating)
            if obj.rating == "N/A":
                obj.rating = "0.0"
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
        return render(request, 'search.html', {'request': request, 'movies': movies})


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


def index(request):
    return render(request, 'moviePage.html', {'request': request})

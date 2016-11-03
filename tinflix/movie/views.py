from django.shortcuts import render
from tinflixer.models import *
from django.http import Http404
from django.template.context import RequestContext
from movie.models import *
import omdb
# Create your views here.
def stage4(request):
    movie = Movie.objects.get(name='The Jungle Book')
    print movie.name
    context = RequestContext(request,
                             {'request': request,
                              'movie': movie})
    return render(request, 'stage4.html', context)


def get_move_detail(name, movie_obj):
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


def search(request):
    if request.method == 'GET':
        name = request.GET.get('q')
        if not name:
            raise Http404
        result = Movie.objects.filter(name__icontains=name).order_by('-popularity')
        if not result.exists():
            movie_obj = Movie(name=name)
            ret = get_move_detail(name, movie_obj)
            if not ret:
                movie_obj.delete()
                result = None
            else:
                result = [ret]
        updated = False
        for obj in result:
            if not obj.popularity:
                get_move_detail(obj.name, obj)
                updated = True
        if updated:
            result = Movie.objects.filter(name__icontains=name).order_by('-popularity')
        context = RequestContext(request,
                                 {'request': request,
                                  'movies': result})
        return render(request, 'search.html', context)


def index(request):
    context = RequestContext(request,
                             {'request': request, })
    return render(request, 'movie.html', context)

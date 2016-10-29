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


def search(request):
    if request.method == 'GET':
        name = request.GET.get('q')
        if not name:
            raise Http404
        try:
            result = Movie.objects.get(name=name)
        except Movie.DoesNotExist:
            api_result = omdb.title(name)
            new_movie_obj = Movie(name=name)
            new_movie_obj.plot = api_result['plot'].encode('utf-8')
            new_movie_obj.duration = api_result['runtime'].encode('utf-8')
            new_movie_obj.release_date = api_result['released'].encode('utf-8')
            new_movie_obj.rating = api_result['imdb_rating'].encode('utf-8')
            new_movie_obj.poster = api_result['poster'].encode('utf-8')
            new_movie_obj.cast_crew = api_result['actors'].encode('utf-8')
            new_movie_obj.genre = api_result['genre'].encode('utf-8')
            new_movie_obj.save()
            result = new_movie_obj
        context = RequestContext(request,
                                 {'request': request,
                                  'user': request.user,
                                  'movie': result})
        return render(request, 'search.html', context)


def index(request):
    context = RequestContext(request,
                             {'request': request, })
    return render(request, 'movie.html', context)

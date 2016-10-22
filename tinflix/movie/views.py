from django.shortcuts import render
from tinflixer.models import *
from django.template.context import RequestContext
from movie.models import *
# Create your views here.
def stage4(request):
    movie = Movie.objects.get(name='The Jungle Book')
    print movie.name
    context = RequestContext(request,
                             {'request': request,
                              'movie': movie})
    return render(request, 'stage4.html', context)

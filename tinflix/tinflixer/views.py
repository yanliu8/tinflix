from django.shortcuts import render_to_response
from django.template.context import RequestContext
# Create your views here.

def index(request):
    context = RequestContext(request,
                             {'request' : request,
                              'user' : request.user})
    return render_to_response("test_login.html", context)



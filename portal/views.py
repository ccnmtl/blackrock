from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model

def index(request):
  return render_to_response('portal/index.html', context_instance=RequestContext(request, {}))

def facet(request):
  return render_to_response('portal/facet.html', context_instance=RequestContext(request, {}))

  

  

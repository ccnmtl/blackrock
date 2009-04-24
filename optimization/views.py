from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree

def index(request, admin_msg=""):

  t = Tree(id=1, species="wo", dbh="5.5", location='POINT(-74.025 41.39)')
  t.save()

  return render_to_response('optimization/index.html',
                            context_instance=RequestContext(request))
                            
def run(request):
  return render_to_response('optimization/run.html')
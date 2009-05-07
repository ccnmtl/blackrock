from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree

def index(request, admin_msg=""):

  t = Tree(id=1, species="wo", dbh="5.5", location='POINT(-74.025 41.39)')
  t.save()
  t2 = Tree(id=2, species="rm", dbh="3.5", location='POINT(-75.025 41.39)')
  t2.save()

  return render_to_response('optimization/index.html',
                            context_instance=RequestContext(request))
                            
def run(request):
  return render_to_response('optimization/run.html')
  
def calculate(request):
  if request.method != 'POST':
    return HttpResponseRedirect("/respiration/")

  numPlots = float(request.REQUEST['numPlots'])
  shape = request.REQUEST['shape']
  diameter = float(request.REQUEST['diameter'])

  results = {}  
  results['results-time'] = "3h 36m"
  results['results-species'] = 10
  results['results-count'] = 321
  results['results-living'] = 124
  results['results-dead'] = 197
  results['results-dbh'] = 23.4
  results['results-density'] = "TBD"
  results['results-basal'] = "TBD"
  results['actual-density'] = "TBD"
  results['actual-basal'] = "TBD"
  
  return HttpResponse(str(results), mimetype="application/javascript")
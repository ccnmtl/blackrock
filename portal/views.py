from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, Context
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
import StringIO
import sys 

def index(request):
  return render_to_response('portal/index.html', context_instance=RequestContext(request, {}))

def facet(request):
  return render_to_response('portal/facet.html', context_instance=RequestContext(request, {}))

@login_required
def admin_rebuild_index(request):
  ctx = Context({ 'server': settings.HAYSTACK_SOLR_URL})
  
  if (request.method == 'POST'):
    sys.stdout = buffer = StringIO.StringIO()
    management.call_command('rebuild_index', interactive=False)
    sys.stdout = sys.__stdout__
    ctx['results'] = buffer.getvalue().split('\n')[1:-2]

  return render_to_response('portal/admin_solr.html', context_instance=ctx)

  

  

  

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
from pagetree.models import Hierarchy
from haystack.query import SearchQuerySet

@login_required
def admin_rebuild_index(request):
  ctx = Context({ 'server': settings.HAYSTACK_SOLR_URL})
  
  if (request.method == 'POST'):
    sys.stdout = buffer = StringIO.StringIO()
    management.call_command('rebuild_index', interactive=False)
    sys.stdout = sys.__stdout__
    ctx['results'] = buffer.getvalue().split('\n')[1:-2]

  return render_to_response('portal/admin_solr.html', context_instance=ctx)

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@rendered_with('portal/page.html')
def page(request,path):
    h = Hierarchy.get_hierarchy('main')
    current_root = h.get_section_from_path(path)
    section = h.get_first_leaf(current_root)
    ancestors = section.get_ancestors()
    
    # Get all assets with valid "infrastructure" facets
    sqs = SearchQuerySet()
    sqs = sqs.facet("infrastructure")
    sqs = sqs.narrow("infrastructure:[* TO *]")
    
    module = None
    if not section.is_root:
        module = ancestors[1]
        
    # retrieve the list of featured assets associated with this section
    return dict(section=section,
                module=module,
                root=ancestors[0],
                infrastructure=sqs)
    
    
    








  

  

  

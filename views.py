from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

def index(request):
  #return HttpResponseRedirect(reverse('blackrock.sampler.views.index'))
  apps = settings.ENABLED_MODULES
  num_public_apps = len([app for app in apps if not app['admin']])
  return render_to_response('index.html',
                            {'apps':apps, 'num_public_apps':num_public_apps},
                            context_instance=RequestContext(request))
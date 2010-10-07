from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from respiration.models import Temperature
import csv, datetime, time, urllib, urllib2
from django.utils import simplejson
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.db import connection, transaction
from django.core.cache import cache
from blackrock_main.models import LastImportDate
import pytz
from blackrock_main.solr import SolrUtilities

@user_passes_test(lambda u: u.is_staff)
def loadsolr_poll(request):
  response = { 'solr_complete': False }
  if cache.has_key('solr_complete'):
    response['solr_complete'] = True
    cache.delete('solr_complete')
    
    if cache.has_key('solr_error'):
      response['solr_error'] = cache.get('solr_error')
      cache.delete('solr_error')
      
    if cache.has_key('solr_created'):
      response['solr_created'] = cache.get('solr_created')
      cache.delete('solr_created')
      
    if cache.has_key('solr_updated'):
      response['solr_updated'] = cache.get('solr_updated')
      cache.delete('solr_updated')
    
    if cache.has_key('solr_import_date'):
      response['solr_import_date'] = cache.get('solr_import_date')
      response['solr_import_time'] = cache.get('solr_import_time')
      cache.delete('solr_import_date')
      cache.delete('solr_import_time')
  
  http_response = HttpResponse(simplejson.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store' 
  return http_response

@user_passes_test(lambda u: u.is_staff)
def previewsolr(request):
  response = {}
  solr = SolrUtilities()
  
  application = request.POST.get('application', '')
  collection_id = request.POST.get('collection_id', '')
  import_classification = request.POST.get('import_classification', '')
  
  last_import_date = solr.get_last_import_date(request, application)
  response['record_count'] = solr.get_count_by_lastmodified(collection_id, import_classification, last_import_date)
    
  if last_import_date:
    response['last_import_date'] = last_import_date.strftime('%Y-%m-%d');
    response['last_import_time'] = last_import_date.strftime('%H:%M:%S');  
  
  http_response = HttpResponse(simplejson.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store' 
  return http_response
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, Context
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model, DateField
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
from django.db.models.fields.related import OneToOneField
import StringIO, sys, urllib
from datetime import datetime, date
from time import strptime
from pagetree.models import Hierarchy
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import user_passes_test
from blackrock_main.solr import SolrUtilities
from portal.models import * 
from decimal import Decimal
from pysolr import Solr, SolrError
from django.core.cache import cache
from blackrock_main.models import LastImportDate
from django.utils import simplejson
from django.utils.tzinfo import FixedOffset


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
    
    module = None
    
    if not section.is_root() and len(ancestors) > 1:
        module = ancestors[1]
        
    # retrieve the list of featured assets associated with this section
    return dict(section=section,
                module=module,
                root=ancestors[0])
    
def process_datasets(xmldoc):
  datasets = []
  for node in xmldoc.getElementsByTagName('int'):
    if node.hasAttribute('name'):
      datasets.append(node.getAttribute('name'))
                      
  return datasets

def process_date(date_string):
  if re.match('\d\d\d\d-\d\d?-\d\d?', date_string):
    t = strptime(date_string, '%Y-%m-%d')
  elif re.match('\d\d\d\d-\d\d?', date_string):
    t = strptime(date_string, '%Y-%m')
  elif re.match('\d\d\d\d', date_string):
    t = strptime(date_string, '%Y')
  
  if t:
    return date(t[0], t[1], t[2])
  
  return None

_dataset_field_map = {  'dataset_id' : 'blackrock_id',
                        'title': 'name',
                        'abstract': 'description',
                        'field_study_data_collection_start_date' : 'collection_start_date',
                        'field_study_data_collection_end_date' : 'collection_end_date',
                        'restriction_on_access' : 'rights_type',
                        'related_files' : 'url',
                        'educational_data_files' : 'url',
                        'lead_investigators' : 'person',
                        'other_investigators' : 'person',
                        'latitude' : 'latitude',
                        'longitude' : 'longitude',
                        'species' : 'facet',
                        'discipline' : 'facet',
                        'scientific_study_type' : 'facet',
                        'keywords' : 'tag'
                      }

def _is_dirty(original_state, new_state):
  for key, value in original_state.iteritems():
     if new_state[key] != None and value != new_state[key]:
       return True
  return False

def process_location(values):
  location = None
  if values.has_key('latitude') and values.has_key('longitude'):
    lat = Decimal(values['latitude'][0].replace('+', ''))
    lng = Decimal(values['longitude'][0])
    location,created = Location.objects.get_or_create(name=values['name'][0], latitude=lat, longitude=lng)
  return location

def process_metadata(result):
  created = False
  dataset = None
  
  try:
    id = result['dataset_id']
    dataset = DataSet.objects.get(blackrock_id=id)
  except DataSet.DoesNotExist:
    dataset = DataSet()
    created = True

  original_state = dict(dataset.__dict__)

  values = {}
  for key, value in result.items():
    if value and key in _dataset_field_map.keys():
        fieldname = _dataset_field_map[key]
        if not values.has_key(fieldname):
          values[fieldname] = []
        if type(value) == type(list()):
          values[fieldname].extend(value)
        else:
          values[fieldname].append(value)
  
  for field in dataset._meta.fields:
    if field.name in values.keys():
      if isinstance(field, DateField):
        value = process_date(values[field.name][0])
      else:
        value = values[field.name][0]
      dataset.__setattr__(field.name, value)
  
  dataset.location = process_location(values)
  if created:
    dataset.save()

  for field in dataset._meta.many_to_many:
    if field.name in values.keys():
      related_model = get_model("portal", field.name)
      for v in values[field.name]:
        if field.name == 'url':
          v = settings.CDRS_SOLR_FILEURL + v
        related_obj, temp_created = related_model.objects.get_or_create(name=v.strip()) 
        dataset.__getattribute__(field.name).add(related_obj)
  
  dataset.audience.add(Audience.objects.get(name='Research'))
  
  if _is_dirty(original_state, dict(dataset.__dict__)):
    dataset.save()
  
  return created
    
@user_passes_test(lambda u: u.is_staff)
def admin_cdrs_import(request):
  if (request.method != 'POST'):
    return render_to_response('portal/admin_cdrs.html', {})
  
  created = 0
  updated = 0
  solr = Solr(settings.CDRS_SOLR_URL)
  
  application = request.POST.get('application', '')
  collection_id = request.POST.get('collection_id', '')
  import_classification = request.POST.get('import_classification', '')
  dt = request.POST.get('last_import_date', '')
  tm =  urllib.unquote(request.POST.get('last_import_time', '00:00'))
  
  q = 'import_classifications:"' + import_classification + '"'
  options = { 'qt': 'forest-data' }
  
  last_import_date = LastImportDate.get_last_import_date(dt, tm, application)
  if last_import_date:
    utc = last_import_date.astimezone(FixedOffset(0))
    q += ' AND last_modified:[' + utc.strftime('%Y-%m-%dT%H:%M:%SZ') + ' TO NOW]'

  try:
    collections = urllib.unquote(collection_id).split(",")
    for c in collections:
      # Get list of datasets in each collection id
      record_count = SolrUtilities().get_count_by_lastmodified(c, import_classification, last_import_date)
      retrieved = 0
      while (retrieved < record_count):
        to_retrieve = min(1000, record_count - retrieved)
        options['collection_id'] = c
        options['start'] = str(retrieved)
        options['rows'] = str(to_retrieve)
      
        results = solr.search(q, **options)
        for result in results:
          if result.has_key('dataset_id'):
            if process_metadata(result):
              created += 1
            else:
              updated += 1
          
        retrieved = retrieved + to_retrieve
        
    # Update the last import date
    lid = LastImportDate.update_last_import_date(application)
    cache.set('solr_import_date', lid.strftime('%Y-%m-%d'))
    cache.set('solr_import_time', lid.strftime('%H:%M:%S'))  
    cache.set('solr_created', created)
    cache.set('solr_updated', updated)
  except Exception, e:
    cache.set('solr_error', str(e)) 
       
  cache.set('solr_complete', True)
  
  response = { 'complete': True }
  http_response = HttpResponse(simplejson.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store' 
  return http_response


@user_passes_test(lambda u: u.is_staff)
def admin_rebuild_index(request):
  ctx = Context({ 'server': settings.HAYSTACK_SOLR_URL})
  
  if (request.method == 'POST'):
    sys.stdout = buffer = StringIO.StringIO()
    management.call_command('rebuild_index', interactive=False)
    sys.stdout = sys.__stdout__
    ctx['results'] = buffer.getvalue().split('\n')[1:-2]

  return render_to_response('portal/admin_solr.html', context_instance=ctx)

def admin_readercycle(request):
    try:
        solr = Solr(settings.HAYSTACK_SOLR_URL)
        solr.readercycle()
        return HttpResponse("Cycled")
    except (IOError, SolrError), e:
        msg = "Failed to cycle Solr %s %s" % (settings.HAYSTACK_SOLR_URL, e)
        return HttpResponse(msg)

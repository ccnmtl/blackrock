from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, Context
from django.shortcuts import render_to_response
from django.db import connection 
from django.db.models import get_model, DateField
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core import management
import StringIO, sys, urllib, datetime, time
from pagetree.models import Hierarchy
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import user_passes_test
from blackrock_main.solr import SolrUtilities
from portal.models import * 
from decimal import Decimal

@user_passes_test(lambda u: u.is_staff)
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
    
    module = None
    if not section.is_root:
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
    t = time.strptime(date_string, '%Y-%m-%d')
  elif re.match('\d\d\d\d-\d\d?', date_string):
    t = time.strptime(date_string, '%Y-%m')
  elif re.match('\d\d\d\d', date_string):
    t = time.strptime(date_string, '%Y')
  
  if t:
    return datetime(t[0], t[1], t[2], t[3], t[4], t[5])
  
  return None

def process_location(values):
  location = None
  if values.has_key('latitude') and values.has_key('longitude'):
    lat = Decimal(values['latitude'][0].replace('+', ''))
    lng = Decimal(values['longitude'][0])
    location,created = Location.objects.get_or_create(name=values['name'][0], latitude=lat, longitude=lng)
  return location

def process_metadata(xmldoc):
  docnode = xmldoc.getElementsByTagName('doc')[0]
  created = False
  dataset_field_map = { 'dataset_id': 'blackrock_id',
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
  
  values = {}
  for node in docnode.childNodes:
    key = dataset_field_map[node.getAttribute("name")]
    if not values.has_key(key):
      values[key] = []
      
    if node.tagName == "str":
      values[key].append(node.firstChild.nodeValue)
    elif node.tagName == "arr":
      for child in node.childNodes:
        values[key].append(child.firstChild.nodeValue)
  
  dataset = None
  try:
    dataset = DataSet.objects.get(blackrock_id=values['blackrock_id'][0])
  except DataSet.DoesNotExist:
    dataset = DataSet()
    created = True
  
  for field in dataset._meta.fields:
    if field.name in values.keys():
      if isinstance(field, DateField):
        value = process_date(values[field.name][0])
      else:
        value = values[field.name][0]
      dataset.__setattr__(field.name, value)
  
  dataset.location = process_location(values)
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
  dataset.save()
  
  return created
    
@user_passes_test(lambda u: u.is_staff)
def admin_cdrs_import(request):
  ctx = Context({ 'server': settings.CDRS_SOLR_URL})
  application = "portal"
  created = 0
  updated = 0
  
  if (request.method == 'POST'):
    try:
      collection_id = request.POST.get('collection_id', '')
      import_classification = request.POST.get('import_classification', '')
      
      collections = collection_id.split(",")
      for c in collections:
        # Get list of datasets in each collection id
        options = {'collection_id': c,
                   'q': 'import_classifications:"' + import_classification + '"',
                   'facet': "true", 
                   'facet.field': "dataset_id",
                   'rows': '0',
                   'facet.mincount': '1' }
        
        solr = SolrUtilities()
        datasets = solr.process_request(options, process_datasets)
        for d in datasets:
          metadata_options = {'collection_id': c,
                              'q': 'import_classifications:"' + import_classification + '"%20AND%20dataset_id:"' + urllib.quote(d) + '"',
                              'rows': '1',
                              'fl': 'dataset_id,title,field_study_data_collection_start_date,field_study_data_collection_end_date,related_files,lead_investigators,abstract,restriction_on_access,educational_data_files,latitude,longitude,other_investigators,species,discipline,audience,keywords' } 
          
          if solr.process_request(metadata_options, process_metadata):
            created += 1
          else:
            updated += 1 
    except Exception, e:
      ctx['error'] = str(e)
       
  ctx['created'] = created
  ctx['updated'] = updated
  return render_to_response('portal/admin_cdrs.html', context_instance=ctx)









  

  

  

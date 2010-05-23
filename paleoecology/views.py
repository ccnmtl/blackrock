from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from blackrock.paleoecology.models import PollenType, PollenSample, CoreSample
import csv
import simplejson as json
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import urlquote
from blackrock_main.solr import SolrUtilities
from django.core.cache import cache
from blackrock_main.models import LastImportDate
import re

def index(request, admin_msg=""):
  return render_to_response('paleoecology/index.html',
                            context_instance=RequestContext(request, {'admin_messages':admin_msg}))

def identification(request):
  return render_to_response('paleoecology/identification.html')

def explore(request):
  samples = CoreSample.objects.all().order_by('depth')
  # TODO figure out from data
  interval = 2.5 # cm
  highest = 1070 + 2.5 # cm
  intervals = [n * interval for n in range(highest / interval)]
  samples = [float(sample.depth) for sample in samples]
  return render_to_response('paleoecology/core-explore.html', {'samples':samples, 'intervals':intervals} )

def getpercents(request):
  depth = request.REQUEST['depth']
  samples = PollenSample.objects.filter(core_sample__depth = depth).filter(percentage__isnull=False).exclude(percentage=0).order_by('pollen__name')
  results = [(s.pollen.display_name, str(s.percentage), int(s.count or 0)) for s in samples]
  names = []
  percents = []
  counts = []
  otherpct = 100
  try:
    names, percents, counts = zip(*results)
    otherpct = 100 - sum([float(i) for i in percents])
    print otherpct
  except:
    pass
  results = {'depth': depth, 'pollen':names, 'percents' : percents, 'counts':counts, 'other':otherpct }

  return HttpResponse(json.dumps(results), mimetype="application/javascript")


@user_passes_test(lambda u: u.is_staff)
def getcsv(request):
  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=coresamples.csv'
  writer = csv.writer(response)

  # write headers
  #headers = ['station', 'year', 'julian day', 'hour', 'avg temp deg C']
  #writer.writerow(headers)

  # write data
  #for t in Temperature.objects.order_by("station", "date"):
  #  julian_day = (t.date - datetime.datetime(year=t.date.year, month=1, day=1)).days + 1
  #  hour = (t.date.hour + 1) * 100
  #  year = t.date.year
  #  row = [t.station, year, julian_day, hour, t.reading];
  #  writer.writerow(row)
  
  return response

@user_passes_test(lambda u: u.is_staff)
def loadcounts(request):
  return loadcsv(request, "counts")

@user_passes_test(lambda u: u.is_staff)
def loadpercents(request):
  return loadcsv(request, "percents")
  
@user_passes_test(lambda u: u.is_staff)
def loadcsv(request, type):
  # if csv file provided, load
  if request.method == 'POST':
    
    try:
      fh = request.FILES['csvfile']
    except:
      return HttpResponseRedirect("/paleoecology/")

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/paleoecology/")

    table = csv.reader(fh)
    headers = table.next()

    for row in table:
       depth = row[0]
       (core, created) = CoreSample.objects.get_or_create(depth=depth)

       for i in range(len(row)):
         if i == 0: continue  # skip row[0], which is the depth
         
         if i == 1 and type == "percents": continue  # skip row[1] in percentages, which is the carbon age

         pollen_name = headers[i].strip()
         (t, created) = PollenType.objects.get_or_create(name=pollen_name)
         (p, created) = PollenSample.objects.get_or_create(core_sample=core, pollen=t)

         if type == "counts":
           p.count = row[i]
         else:
           p.percentage = row[i]
         p.save()

         # hack to fix Pinus and Asteraceae counts
         if type == "counts" :
           if pollen_name in ["Pinus subg. Pinus", "Pinus subg. Strobus", "Pinus undiff."]:
             (second, created) = PollenType.objects.get_or_create(name="Pinus", display_name="Pinus (Pine)")
             (p, created) = PollenSample.objects.get_or_create(core_sample=core, pollen=second)
             p.count = (p.count or 0) + int(row[i])
             p.save()

           if pollen_name in ["Asteraceae subf. Asteroideae undiff.", "Asteraceae subf. Cichorioideae"]:
             (second, created) = PollenType.objects.get_or_create(name="Asteraceae", display_name="Asteraceae (Ragweed etc.)")
             (p, created) = PollenSample.objects.get_or_create(core_sample=core, pollen=second)
             p.count = (p.count or 0) + int(row[i])
             p.save()

    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/paleoecology/")

_collection_id = 'paleo'
_import_set_type = 'cleaned'
_sets = ['corrected_paleo Pollen Types', 'corrected_paleo 15 Pollen Types', 'corrected_paleo Raw Counts of 65 Pollen Types']
             
@user_passes_test(lambda u: u.is_staff)
def loadsolr(request):
  created_count = 0
  updated_count = 0
  
  PollenSample.objects.all().delete();
  
  try:
    sets = SolrUtilities.get_importsets_by_lastmodified(_collection_id, _import_set_type, None, request.POST.get('import_set', ''))
    
    for import_set in sets:
      if import_set == 'corrected_paleo Pollen Types':
        created, updated = _import_pollen_types(import_set, sets[import_set])
        created_count += created
        updated_count += updated
        
      if import_set == 'corrected_paleo Raw Counts of 65 Pollen Types':
        created, updated = _import_counts(import_set, sets[import_set], 'count')
        created_count += created
        updated_count += updated
        
      if import_set == 'corrected_paleo 15 Pollen Types':
        created, updated = _import_counts(import_set, sets[import_set], 'percentage')
        created_count = created_count + created
        updated_count = updated_count + updated

    cache.set('solr_created', created_count)
    cache.set('solr_updated', updated_count)
  except Exception,e:
    cache.set('solr_error', str(e)) 
  
  cache.set('solr_complete', True)
  
  response = { 'complete': True }
  http_response = HttpResponse(json.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store' 
  return http_response

def _import_pollen_types(import_set, count):
  created_count = 0
  updated_count = 0
  url = SolrUtilities.base_query() + '&collection_id=' + _collection_id  + '&q=import_set:"' + urlquote(import_set) + '"&rows=' + str(count) + '&fl=plant_name,plant_type'
  xmldoc = SolrUtilities.solr_request(url)
  
  for node in xmldoc.getElementsByTagName('doc'):
    plant_name = None
    plant_type = None
    for child in node.childNodes:
      name = child.getAttribute('name')
      if (name == 'plant_name'):
        plant_name = _normalize_pollen_name(child.childNodes[0].nodeValue)
      elif (name == 'plant_type'):
        plant_type = child.childNodes[0].nodeValue
    
    pt, created = _get_or_create_pollen_type(plant_name, plant_type)
    
    if created:
      print 'New Pollen Type found: ' + pt.name
      created_count = created_count + 1
    else:
      updated_count = updated_count + 1
  
  # a few manual entries for summary purposes 
  _get_or_create_pollen_type("Pinus", "A", "Pinus (Pine)")
  _get_or_create_pollen_type("Asteraceae", "B", "Asteraceae (Ragweed etc.)")
            
  xmldoc.unlink()
  
  return created_count, updated_count

def _import_counts(import_set, count, fieldname):
  created_count = 0
  updated_count = 0
  exceptions = ['longitude', 'latitude', 'depth_(cm)']
  
  url = SolrUtilities.base_query() + '&collection_id=' + _collection_id  + '&q=import_set:"' + urlquote(import_set) + '"&rows=' + str(count)
  xmldoc = SolrUtilities.solr_request(url)
  
  pinus_pollen = PollenType.objects.get(name='Pinus')
  asteraceae_pollen = PollenType.objects.get(name='Asteraceae')
  
  for node in xmldoc.getElementsByTagName('doc'):
    core_sample = None
    
    for child in node.childNodes:
      name = child.getAttribute('name')
      if (name == 'record_subject'):
        # record_subject always comes first. the logic counts on this order.
        core_sample, created = _add_core_sample(child.childNodes[0].nodeValue)
      elif child.tagName == 'double' and name not in exceptions:
        pollen_name = _normalize_pollen_name(name.strip().replace('_', ' ')) # solr names for count/percentages come in lowercase with underscores replacing spaces
        try:
          pollen_type = PollenType.objects.get(name__iexact=pollen_name)
          pollen_count, created = _update_or_create_pollen_sample(pollen_type, core_sample, fieldname, child.childNodes[0].nodeValue)
          
          if created:
            created_count += 1
          else:
            updated_count += 1
            
          if fieldname == 'count':
            if pollen_name.lower() in ["pinus subg. pinus", "pinus subg. strobus", "pinus undiff."]:
              _update_or_create_pollen_sample(pinus_pollen, core_sample, fieldname, child.childNodes[0].nodeValue, summarize=True)
            elif pollen_name.lower() in ["asteraceae subf. asteroideae undiff.", "asteraceae subf. cichorioideae"]:
              _update_or_create_pollen_sample(asteraceae_pollen, core_sample, fieldname, child.childNodes[0].nodeValue, summarize=True)
        except PollenType.DoesNotExist:
          print 'Pollen type: %s Does Not Exist' % pollen_name

  xmldoc.unlink()
  return created_count, updated_count

def _get_or_create_pollen_type(name, type, display_name=""):
  print '_get_or_create_pollen_type' + name + ' ' + type
  pt, created = PollenType.objects.get_or_create(name__iexact=name)
  
  if len(type) == 1: # Organic Matter's type is gibberish
    pt.type = type
    
  if len(display_name) > 0:
    pt.display_name = display_name;
  
  pt.save()

  if created:
    print 'New pollen type created: %s' % (name)
  print '~_get_or_create_pollen_type'
  return pt, created

# Format of record_subject is Depth of XX cm. Parse out the XX, find or create a core sample. Continue.
def _add_core_sample(depth):
  d = re.search('\d+', depth)
  return CoreSample.objects.get_or_create(depth=d.group(0))
  
def _update_or_create_pollen_sample(pollen_type, core_sample, fieldname, value, summarize=False):
  ps, created = PollenSample.objects.get_or_create(pollen=pollen_type, core_sample=core_sample)
  
  value = float(value)    
  if summarize:
    oldval = ps.__getattribute__(fieldname)
    if oldval:
      value += float(oldval)
  ps.__setattr__(fieldname, str(value))

  ps.save()
  
  return ps, created

def _normalize_pollen_name(pollen_name):
  translate = { 
    'poaceae':'Gramineae', 
    'organic matter (percent dry mass)':'Organic matter', 
    'o/c':'Ostrya/Carpinus', 
    'asteraceae (incl ragweed)': 'Asteraceae', 
    'birch':'Betula',
    'spruce': 'Picea',
    'castanea': 'Castanea dentata',
    'tsuga': 'Tsuga canadensis',
    'fagus': 'Fagus grandifolia', 
  }
  
  if pollen_name.lower() in translate:
    return translate[pollen_name.lower()]
  else:
    return pollen_name
  
      
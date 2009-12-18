from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from blackrock.paleoecology.models import PollenType, PollenSample, CoreSample
import csv
import simplejson as json
#import datetime

def index(request, admin_msg=""):
  return render_to_response('paleoecology/index.html',
                            context_instance=RequestContext(request, {'admin_messages':admin_msg}))

def identification(request):
  return render_to_response('paleoecology/identification.html')

def explore(request):
  samples = PollenSample.objects.all()
  return render_to_response('paleoecology/core-explore.html', {'samples':samples} )

def results(request):
  pollen = [p.name for p in PollenType.objects.all().order_by('name') if p.name not in ["Pinus", "Asteraceae (incl ragweed)"]]
  samples = CoreSample.objects.all().order_by('depth')
  
  # summary row (totals)
  num_samples = samples.count()
  num_species = len(pollen)
  num_specimens = 0

  totals = ["TOTAL: %s" % num_samples, ""]

  for ptype in pollen:
    total = sum([p.count for p in PollenSample.objects.filter(pollen__name=ptype)])
    totals.append(total)
    num_specimens += total
      
  return render_to_response('paleoecology/core-results.html', {'pollen':pollen, 'samples':samples, #'counts':counts,
                                                               'numsamples':num_samples, 'numspecies':num_species,
                                                               'numspecimens':int(num_specimens), 'totals':totals} )

def getrow(request):
  depth = request.REQUEST['depth']
  samples = PollenSample.objects.filter(core_sample__depth = depth).order_by('pollen__name').exclude(pollen__name="Pinus").exclude(pollen__name="Asteraceae (incl ragweed)")
  results = {'depth': depth, 'counts' : [int(sample.count) for sample in samples] }

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
       if created: core.save()

       for i in range(len(row)):
         if i == 0: continue  # skip row[0], which is the depth

         pollen_name = headers[i].strip()
         (t, created) = PollenType.objects.get_or_create(name=pollen_name)
         if created: t.save()

         (p, created) = PollenSample.objects.get_or_create(core_sample=core, pollen=t)

         if type == "counts":
           p.count = row[i]
         else:
           p.percentage = row[i]
         p.save()

    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/paleoecology/")
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from blackrock.paleoecology.models import PollenType, PollenSample
import csv
#import datetime

def index(request, admin_msg=""):
  return render_to_response('paleoecology/index.html',
                            context_instance=RequestContext(request, {'admin_messages':admin_msg}))

def identification(request):
  return render_to_response('paleoecology/identification.html')

def coresample(request):
  p = PollenType(name="test", type="A")
  p.save()
  pollen = PollenType.objects.all()
  return render_to_response('paleoecology/coresample.html', {'pollen':pollen} )

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
       for i in range(len(row)):
         if i == 0: continue

         (t, created) = PollenType.objects.get_or_create(name=headers[i])
         (p, created) = PollenSample.objects.get_or_create(depth=row[0], pollen=t)
         p.count = row[i]
         t.save()
         p.save()

    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/paleoecology/")
  
@user_passes_test(lambda u: u.is_staff)
def loadpercents(request):
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
       for i in range(len(row)):
         if i == 0: continue

         (t, created) = PollenType.objects.get_or_create(name=headers[i])
         (p, created) = PollenSample.objects.get_or_create(depth=row[0], pollen=t)
         p.percentage = row[i]
         p.save()
         t.save()       

    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/paleoecology/")
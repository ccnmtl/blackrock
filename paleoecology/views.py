from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
#from blackrock.paleoecology.models import CoreSample
#import csv, datetime

def index(request, admin_msg=""):
  return render_to_response('paleoecology/index.html',
                            context_instance=RequestContext(request, {'admin_messages':admin_msg}))

def identification(request):
  return render_to_response('paleoecology/identification.html')

def coresample(request):
  return render_to_response('paleoecology/coresample.html')

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
def loadcsv(request):
  # if csv file provided, loadcsv
  if request.method == 'POST':
    
    try:
      fh = request.FILES['csvfile']
    except:
      return HttpResponseRedirect("/paleoecology/")

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/paleoecology/")

    #fh = fh['content'].split('\n')
    table = csv.reader(fh)

    headers = table.next()
    expected_headers = "station, year, julian day, hour, avg temp deg C"
    for i in range(0, len(headers)):
      header = headers[i].lower()
      if header == "station":
        station_idx = i
      elif header == "year":
        year_idx = i
      elif header == "julian day":
        day_idx = i
      elif header == "hour":
        hour_idx = i
      elif header == "avg temp deg c":
        temp_idx = i
      else:
        return HttpResponse("Unsupported header '%s'.  We expect: %s." % (header, expected_headers))
        
    # make sure all headers are defined
    if not (vars().has_key('station_idx') and vars().has_key('year_idx') and
            vars().has_key('day_idx') and vars().has_key('hour_idx') and
            vars().has_key('temp_idx')):
      return HttpResponse("Error: Missing header.  We expect: %s" % expected_headers)
     
    # clear existing data
    CoreSample.objects.all().delete()

    #for row in table:
       #print "processing %s" % row
    #   station = row[station_idx]
    #   year = row[year_idx]
    #   julian_days = row[day_idx]
    #   hour = row[hour_idx]
    #   temp = row[temp_idx]

    #   if temp != "":
    #     (t, created) = Temperature.objects.get_or_create(station=station, date=dt)
    #     t.reading = float(temp)
    #     next_expected_timestamp = dt + datetime.timedelta(hours=1)
         #last_timestamp_of_year = datetime.datetime(year=int(year)+1, day=1, month=1, hour=0) - datetime.timedelta(hours=1)
         #print last_timestamp_of_year
    #     if dt == datetime.datetime(year=int(year), month=12, day=31, hour=23):  # 12/31 11pm (last timestamp of the year)
           #print "last timestamp of year; no expected next value"
    #       next_expected_timestamp = None
    #     last_valid_temp = temp
    #     t.save()
           
    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/paleoecology/")
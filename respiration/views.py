from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from blackrock.respiration.models import Temperature
import csv, datetime

def index(request, admin_msg=""):
  return render_to_response('respiration/index.html',
                            context_instance=RequestContext(request, {'admin_messages':admin_msg}))

def leaf(request):
  # get passed-in defaults
  basetemp = 0
  try:
    basetemp = request.POST['scenario1-base-temp']
  except:
    pass
    
  scenario_options = {'basetemp':0, 'name':'Scenario 1', 'leafarea':1, 'startdate':'1/1', 'enddate':'12/31', 'deltat':'',
                      'fieldstation':'', 'year':''}
  try:
    scenario_options['name'] = request.POST['scenario1-name']
    scenario_options['year'] = request.POST['scenario1-year']
    scenario_options['fieldstation'] = request.POST['scenario1-fieldstation']
    scenario_options['leafarea'] = request.POST['scenario1-leafarea']
    scenario_options['startdate'] = request.POST['scenario1-startdate']
    scenario_options['enddate'] = request.POST['scenario1-enddate']
    scenario_options['deltat'] = request.POST['scenario1-delta-t']
  except:
    pass
    
  specieslist = []
  try:
    specieslist = request.POST['scenario1-species'].split(",")
  except:
    pass
    
  myspecies = []
  for s in specieslist:
    if(s != ""):
      species = {}
      species['name'] = request.POST[s+'-name']
      species['E0'] = request.POST[s+'-E0']
      species['R0'] = request.POST[s+'-R0']
      species['percent'] = request.POST[s+'-percent']
      myspecies.append(species)

  return render_to_response('respiration/leaf.html', {'basetemp':basetemp, 'numspecies':len(myspecies), 'specieslist':myspecies,
                                                      'scenario_options':scenario_options})

def forest(request):
  stations = Temperature.objects.values('station').order_by('station').distinct()
  station_names = [item['station'] for item in stations]
  # get valid years for each station
  year_options = {}
  for station in station_names:
    years = [item.year for item in Temperature.objects.filter(station=station).dates('date','year')]
    year_options[station] = str(years)

  # get passed-in defaults
  scenario_options = {'basetemp':0, 'name':'Scenario 1', 'leafarea':1, 'startdate':'1/1', 'enddate':'12/31', 'deltat':'',
                      'fieldstation':'', 'year':''}
  try:
    scenario_options['basetemp'] = request.POST['base-temp']
    scenario_options['name'] = request.POST['scenario1-name']
    scenario_options['year'] = request.POST['scenario1-year']
    scenario_options['fieldstation'] = request.POST['scenario1-fieldstation']
    scenario_options['leafarea'] = request.POST['scenario1-leafarea']
    scenario_options['startdate'] = request.POST['scenario1-startdate']
    scenario_options['enddate'] = request.POST['scenario1-enddate']
    scenario_options['deltat'] = request.POST['scenario1-delta-t']
  except:
    pass
    
  specieslist = []
  try:
    specieslist = request.POST['specieslist'].split(",")
  except:
    pass

  myspecies = []
  for s in specieslist:
    if(s != ""):
      species = {}
      species['name'] = request.POST[s+'-name']
      species['E0'] = request.POST[s+'-E0']
      species['R0'] = request.POST[s+'-R0']
      try:
        species['percent'] = request.POST[s+'-percent']
      except:
        species['percent'] = ''
      myspecies.append(species)
      
  return render_to_response('respiration/forest.html', {'stations':station_names, 'years':year_options,
                                                        'numspecies':len(myspecies), 'specieslist':myspecies,
                                                        'scenario_options':scenario_options})

def getsum(request):
  #if request.method != 'POST':
  #  return HttpResponseRedirect("/respiration/")
  R0 = float(request.REQUEST['R0'])
  E0 = float(request.REQUEST['E0'])
  T0 = float(request.REQUEST['t0'])
  deltaT = 0.0;
  try:
    deltaT = float(request.REQUEST['delta'])
  except:
    deltaT = 0.0;

  start = request.REQUEST['start']
  startpieces = start.split('/')
  startfinal = datetime.datetime(int(startpieces[2]), int(startpieces[0]), int(startpieces[1]))
  end = request.REQUEST['end']
  endpieces = end.split('/')
  endfinal = datetime.datetime(int(endpieces[2]), int(endpieces[0]), int(endpieces[1]))

  station = request.REQUEST['station']
  (total, time) = Temperature.arrhenius_sum(E0,R0,T0,deltaT,startfinal,endfinal,station)
  total_mol = total / 1000000
  json = '{"total": %s}' % round(total_mol,2)
  return HttpResponse(json, mimetype="application/javascript")


@user_passes_test(lambda u: u.is_staff)
def getcsv(request):
  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=temperature_readings.csv'
  writer = csv.writer(response)

  # write headers
  headers = ['station', 'year', 'julian day', 'hour', 'avg temp deg C']
  writer.writerow(headers)

  # write data
  for t in Temperature.objects.order_by("station", "date"):
    julian_day = (t.date - datetime.datetime(year=t.date.year, month=1, day=1)).days + 1
    hour = t.date.hour * 100
    year = t.date.year
    if(hour == 0):
      hour = 2400
      newdate = t.date - datetime.timedelta(days=1)
      year = newdate.year
      julian_day = (newdate - datetime.datetime(year=year, month=1, day=1)).days + 1
    row = [t.station, year, julian_day, hour, t.reading];
    writer.writerow(row)
  
  return response
  
@user_passes_test(lambda u: u.is_staff)
def loadcsv(request):
  # if csv file provided, loadcsv
  if request.method == 'POST':
    
    try:
      fh = request.FILES['csvfile']
    except:
      return HttpResponseRedirect("/respiration/")

    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect("/respiration/")

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
    Temperature.objects.all().delete()

    next_expected_timestamp = None
    last_valid_temp = None

    for row in table:
       #print "processing %s" % row
       station = row[station_idx]
       year = row[year_idx]
       julian_days = row[day_idx]
       hour = row[hour_idx]
       temp = row[temp_idx]

       # adjust hour from "military" to 0-23, and 2400 becomes 0 of the next day
       normalized_hour = int(hour)/100
       if normalized_hour == 24:
         normalized_hour = 0
         julian_days = int(julian_days) + 1

       delta = datetime.timedelta(days=int(julian_days)-1)
       dt = datetime.datetime(year=int(year), month=1, day=1, hour=normalized_hour)
       dt = dt + delta
       
       if temp == "" or float(temp) < -100 or float(temp) > 100:
         if last_valid_temp is not None:
           temp = last_valid_temp
         else:
           temp = 0

       if next_expected_timestamp is not None and dt != next_expected_timestamp:
         # if dt < expected we just assume it is a duplicate of data we already have
         while(dt > next_expected_timestamp and dt.year == next_expected_timestamp.year):
           (t, created) = Temperature.objects.get_or_create(station=station, date=next_expected_timestamp)
           if created:
             #print "input data: %s %s %s" % (year, julian_days, hour)
             #julian_day = (dt - datetime.datetime(year=int(year), month=1, day=1)).days
             #print "missing data for %s: expected %s but got %s" % (station, next_expected_timestamp, dt)
             #print "(julian day %s) " % julian_day
             #print "missing data: no data for %s" % next_expected_timestamp
             if last_valid_temp is not None:
               #print "using last known value of %s" % last_valid_temp
               t.reading = float(last_valid_temp)
             else:
               #print "using current value of %s" % temp
               t.reading = float(temp)
             t.save()
             next_expected_timestamp = next_expected_timestamp + datetime.timedelta(hours=1)
           
       if temp != "":
         (t, created) = Temperature.objects.get_or_create(station=station, date=dt)
         t.reading = float(temp)
         next_expected_timestamp = dt + datetime.timedelta(hours=1)
         #last_timestamp_of_year = datetime.datetime(year=int(year)+1, day=1, month=1, hour=0) - datetime.timedelta(hours=1)
         #print last_timestamp_of_year
         if dt == datetime.datetime(year=int(year), month=12, day=31, hour=23):  # 12/31 11pm (last timestamp of the year)
           #print "last timestamp of year; no expected next value"
           next_expected_timestamp = None
         last_valid_temp = temp
         t.save()
           
    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/respiration/")
  #return render_to_response('respiration/index.html',
  #                          context_instance=RequestContext(request,{'admin_messages':admin_msg})
  #                        )

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
    year_options[station] = str(years).replace('[','(').replace(']',')')

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
  print request.POST
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
       
       # skipping bad data for now
       if temp != "":
         (t, created) = Temperature.objects.get_or_create(station=station, date=dt)
         t.reading = float(temp)
         t.save()
           
    admin_msg = "Successfully imported data."

    return index(request, admin_msg)
  
  return HttpResponseRedirect("/respiration/")
  #return render_to_response('respiration/index.html',
  #                          context_instance=RequestContext(request,{'admin_messages':admin_msg})
  #                        )
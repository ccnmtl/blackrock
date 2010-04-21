from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from blackrock.respiration.models import Temperature
import csv, datetime, time, urllib, urllib2
from django.utils import simplejson
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset

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
      
  return render_to_response('respiration/forest.html', {
      'stations':station_names, 
      'years':year_options,
      'numspecies':len(myspecies),
      'specieslist':myspecies,
      'scenario_options':scenario_options,
      })

def getsum(request):
  if request.method != 'POST':
    return HttpResponseRedirect("/respiration/")
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
  # we add 1 day so we can do < enddate and include all values for the end date (start and end date are both inclusive)
  endfinal = datetime.datetime(int(endpieces[2]), int(endpieces[0]), int(endpieces[1])) + datetime.timedelta(days=1)

  station = request.REQUEST['station']
  (total, time) = Temperature.arrhenius_sum(E0,R0,T0,deltaT,startfinal,endfinal,station)
  total_mol = total / 1000000
  json = '{"total": %s}' % round(total_mol,2)
  return HttpResponse(json, mimetype="application/javascript")

def getcsv(request):

  filters = dict((f, request.GET.get(f)) for f in _filters)
  
  if sum(bool(f) for f in filters.values()) != len(filters):
    if not request.user.is_staff:
      return HttpResponseForbidden("you must provide a station, a year and a season range")
    temperatures = Temperature.objects.all()
  else:
    year = int(filters['year'])
    start = filters['start'].split('/')
    start_month, start_day = int(start[0]), int(start[1])
    end = filters['end'].split('/')
    end_month, end_day = int(end[0]), int(end[1])
    start = datetime.datetime(year=year, month=start_month, day=start_day)
    end = datetime.datetime(year=year, month=end_month, day=end_day)

    end += datetime.timedelta(hours=23, minutes=59)
    
    temperatures = Temperature.objects.filter(station=filters['station'],
                                              date__range=(start, end))
    
  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=temperature_readings.csv'
  writer = csv.writer(response)

  # write headers
  headers = ['station', 'year', 'julian day', 'hour', 'avg temp deg C']
  writer.writerow(headers)

  # write data
  temperatures = temperatures.order_by("station", "date")
  for t in temperatures:
    julian_day = (t.date - datetime.datetime(year=t.date.year, month=1, day=1)).days + 1
    hour = (t.date.hour + 1) * 100
    year = t.date.year
    #if(hour == 0):
    #  hour = 2400
    #  newdate = t.date - datetime.timedelta(days=1)
    #  year = newdate.year
    #  julian_day = (newdate - datetime.datetime(year=year, month=1, day=1)).days + 1
    row = [t.station, year, julian_day, hour, t.reading];
    writer.writerow(row)
  
  return response
  
@user_passes_test(lambda u: u.is_staff)
def loadcsv(request):
  response = { 'rowcount': 0 }
  
  # if csv file provided, loadcsv
  if request.method != 'POST' or 'csvfile' not in request.FILES:
    return HttpResponse('No csv file specified')
  else:   
    fh = request.FILES['csvfile']
  
    # TODO: error checking (correct file type, etc.)
  
    table = csv.reader(fh)
  
    headers = table.next()
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
        
    # make sure all headers are defined
    if not (vars().has_key('station_idx') and vars().has_key('year_idx') and
            vars().has_key('day_idx') and vars().has_key('hour_idx') and
            vars().has_key('temp_idx')):
      expected_headers = "station, year, julian day, hour, avg temp deg C"
      return HttpResponse("Error: Missing header.  We expect: %s" % expected_headers)
    else:
      if request.POST.get('delete') == 'on':
        qs = Temperature.objects.all()
        response['deleted'] = qs.count() 
        qs.delete()
    
      next_expected_timestamp = None
      last_valid_temp = None
      prev_station = None
      
      for row in table:
        station = row[station_idx]
        year = row[year_idx]
        julian_days = row[day_idx]
        hour = row[hour_idx]
        temp = row[temp_idx]
    
        # adjust hour from "military" to 0-23, and 2400 becomes 0 of the next day
        normalized_hour = int(hour)/100 - 1
        #if normalized_hour == 24:
        #  normalized_hour = 0
        # julian_days = int(julian_days) + 1
    
        delta = datetime.timedelta(days=int(julian_days)-1)
        dt = datetime.datetime(year=int(year), month=1, day=1, hour=normalized_hour)
        dt = dt + delta
         
        (next_expected_timestamp, last_valid_temp, prev_station, created) = _process_row(dt, station, temp, next_expected_timestamp, last_valid_temp, prev_station)
        response['rowcount'] = response['rowcount'] + created
    
  return HttpResponseRedirect('/admin/respiration/temperature')

def _process_row(record_datetime, station, temp, next_expected_timestamp, last_valid_temp, prev_station):

  if temp == "" or float(temp) < -100 or float(temp) > 100:
    if last_valid_temp is not None and station == prev_station:
      temp = last_valid_temp
    else:
      temp = 0
      
  count = 0
  
  # if data is missing, fill in the blanks with the last valid temp
  if next_expected_timestamp is not None and record_datetime != next_expected_timestamp:
    # if dt < expected we just assume it is a duplicate of data we already have
    while(record_datetime > next_expected_timestamp and record_datetime.year == next_expected_timestamp.year):
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
        count = count + 1
         
  if temp != "":
    (t, created) = Temperature.objects.get_or_create(station=station, date=record_datetime)
        
    if created:
      count = count + 1  
    #else:
    #  print 'Record already exists for this date/time slot: %s %s %f' % (station, record_datetime.ctime(), float(temp))

    t.reading = float(temp)
    next_expected_timestamp = record_datetime + datetime.timedelta(hours=1)
    #last_timestamp_of_year = datetime.datetime(year=int(year)+1, day=1, month=1, hour=0) - datetime.timedelta(hours=1)
    #print last_timestamp_of_year
    if record_datetime.month == 12 and record_datetime.day == 31 and record_datetime.hour == 23:  # 12/31 11pm (last timestamp of the year)
      #print "last timestamp of year; no expected next value"
      next_expected_timestamp = None
    last_valid_temp = temp
    t.save()
    
  return (next_expected_timestamp, last_valid_temp, station, count)
         
  
def _string_to_datetime(date_string, time_string):
  try:
    t = time.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M')
    dt = datetime.datetime(t[0], t[1], t[2], t[3], t[4])
    return dt
  except:
    return None
 
def _solr_string_to_datetime(date_string):
  try:
    t = time.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    utc = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=FixedOffset(0))
    est = utc.astimezone(FixedOffset(-300))
    return est
  except:
    return None
  
def _solr_request(url):
  response = urllib2.urlopen(url)
  xmldoc = minidom.parse(response)
  response.close()
  return xmldoc

# Retrieve the requested import sets
# If no import_set is specified, retrieve all "educational" sets that have rows
def _solr_get_sets(base_query, import_set):
  sets = {}
  count_query = base_query + 'facet=true&facet.field=import_set&rows=0&q=import_set_type:"educational"'
  if (len(import_set) > 0):
    count_query = count_query + '%20AND%20import_set:"' + import_set + '"'

  xmldoc = _solr_request(count_query)
  for node in xmldoc.getElementsByTagName('int'):
    if node.hasAttribute('name') and int(node.childNodes[0].nodeValue) > 0:
      sets[node.getAttribute('name')] = int(node.childNodes[0].nodeValue)
  xmldoc.unlink()
  
  return sets
  
def loadsolr(request):
  response = { 'rowcount': 0 }
  try:
    base_query = urllib.unquote(request.POST['base_query'])
    delete_data = request.POST.get('delete_data', 'false') == 'true'
    station = urllib.unquote(request.POST['station'])
    start_date = _string_to_datetime(request.POST['start_date'], '00:00')
    end_date = _string_to_datetime(request.POST['end_date'], '23:59')
    
    if (delete_data):
      response['deleted'] = Temperature.selective_delete(station, start_date, end_date)
      
    sets = _solr_get_sets(base_query, urllib.unquote(request.POST.get('import_set', "")))
    
    for import_set in sets:
      next_expected_timestamp = None
      last_valid_temp = None
      prev_station = None
      row_count = sets[import_set]
        
      retrieved = 0 
      while (retrieved < row_count):
        to_retrieve = min(1000, row_count - retrieved)
        data_query = base_query + 'q=import_set:"' + import_set + '"&fl=collection_id,import_set,record_datetime,record_subject,location_name,latitude,longitude,temp_c_avg,temp_avg&sort=record_datetime%20asc'
        url = '%s&start=%d&rows=%d' % (data_query, retrieved, to_retrieve)
        xmldoc = _solr_request(url)
        for node in xmldoc.getElementsByTagName('doc'):
          station = None
          dt = None
          temp = None
          for child in node.childNodes:
            name = child.getAttribute('name')
            if (name == 'location_name'):
              station = child.childNodes[0].nodeValue.rstrip(' Station')
            elif (name == 'temp_c_avg' or name == 'temp_avg'):
              temp = child.childNodes[0].nodeValue
            elif (name == 'record_datetime'):
              dt = _solr_string_to_datetime(child.childNodes[0].nodeValue)
          
          if (station and dt and temp):
            (next_expected_timestamp, last_valid_temp, prev_station, created) = _process_row(dt, station, float(temp), next_expected_timestamp, last_valid_temp, prev_station)
            response['rowcount'] = response['rowcount'] + created
            
        xmldoc.unlink()
        retrieved = retrieved + to_retrieve
  except:
    import sys
    response['message'] = "Unexpected error:", sys.exc_info()[0]
  
  http_response = HttpResponse(simplejson.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store'
  return http_response  
      

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from respiration.models import Temperature, StationMapping
import csv, datetime, time, urllib, urllib2
from django.utils import simplejson
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.db import connection, transaction
from django.core.cache import cache
from blackrock_main.models import LastImportDate
import pytz
from blackrock_main.solr import SolrUtilities
from decimal import Decimal, ROUND_HALF_UP

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

_filters = 'station start end year'.split()
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
  headers = ['station', 'year', 'julian day', 'hour', 'avg temp deg C', 'data source']
  writer.writerow(headers)

  # write data
  temperatures = temperatures.order_by("station", "date")
  for t in temperatures:
    julian_day = (t.date - datetime.datetime(year=t.date.year, month=1, day=1)).days + 1
    hour = (t.date.hour + 1) * 100
    year = t.date.year
#    if(hour == 0):
#      hour = 2400
#      newdate = t.date - datetime.timedelta(days=1)
#      year = newdate.year
#      julian_day = (newdate - datetime.datetime(year=year, month=1, day=1)).days + 1
    row = [t.station, year, julian_day, hour, t.reading, t.data_source];
    writer.writerow(row)
  
  return response
  
@user_passes_test(lambda u: u.is_staff)
@transaction.commit_on_success
def loadcsv(request):
  cursor = connection.cursor()
  
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
         
        (next_expected_timestamp, last_valid_temp, prev_station, created, updated) = _process_row(cursor, dt, station, temp, next_expected_timestamp, last_valid_temp, prev_station)
        
  transaction.set_dirty()
  return HttpResponseRedirect('/admin/respiration/temperature')

def _update_or_insert(cursor, record_datetime, station, temp, data_source):
  created = False
  cursor.execute("UPDATE respiration_temperature SET reading=%s, data_source=%s where station=%s and date=%s", [str(temp), data_source, station, record_datetime.strftime('%Y-%m-%d %H:%M:%S%z')])
  if cursor.rowcount < 1:
    cursor.execute('INSERT into respiration_temperature values(DEFAULT, %s, %s, %s, 1, %s)', [station, record_datetime.strftime('%Y-%m-%d %H:%M:%S%z'), str(temp), data_source]);
    created = cursor.rowcount > 0
    
  return created 

def _process_row(cursor, record_datetime, station, temp, next_expected_timestamp, last_valid_temp, prev_station):
  
  if temp == "" or float(temp) < -100 or float(temp) > 100:
    if last_valid_temp is not None and station == prev_station:
      temp = last_valid_temp
    else:
      temp = 0
      
  created_count = 0
  updated_count = 0
  
  # if data is missing, fill in the blanks with the last valid temp
  if next_expected_timestamp is not None and record_datetime != next_expected_timestamp:
    # if dt < expected we just assume it is a duplicate of data we already have
    while(record_datetime > next_expected_timestamp and record_datetime.year == next_expected_timestamp.year):
      if last_valid_temp is not None:
        reading = float(last_valid_temp)
      else:
        reading = float(temp)
          
      created = _update_or_insert(cursor, next_expected_timestamp, station, reading, 'mock')
      next_expected_timestamp = next_expected_timestamp + datetime.timedelta(hours=1)
      
      if created:
        created_count = created_count + 1
      else:
        updated_count = updated_count + 1
         
  if temp != "":
    created = _update_or_insert(cursor, record_datetime, station, float(temp), 'original')
        
    if created:
      created_count = created_count + 1
    else:
      updated_count = updated_count + 1  

    next_expected_timestamp = record_datetime + datetime.timedelta(hours=1)
    
    if record_datetime.month == 12 and record_datetime.day == 31 and record_datetime.hour == 23:  # 12/31 11pm (last timestamp of the year)
      next_expected_timestamp = None
    last_valid_temp = temp
    
  return (next_expected_timestamp, last_valid_temp, station, created_count, updated_count)

@user_passes_test(lambda u: u.is_staff)
@transaction.commit_on_success
def loadsolr(request):
  import_set = request.POST.get('import_set', '')
  collection_id = request.POST.get('collection_id', '')
  import_set_type = request.POST.get('import_set_type', '')
  facet_field = request.POST.get('facet_field', '')
  
  stations = {}
  for sm in StationMapping.objects.all():
    stations[sm.abbreviation] = sm.station
  
  created_count = 0
  updated_count = 0
  try:
    cursor = connection.cursor()
    last_import_date = SolrUtilities.get_last_import_date(request, 'respiration')
    sets = SolrUtilities.get_importsets_by_lastmodified(collection_id, import_set_type, last_import_date, import_set, facet_field)
    
    for import_set in sets:
      if import_set.find("_") > 0:
        next_expected_timestamp = None
        last_valid_temp = None
        prev_station = None
        retrieved = 0
         
        while (retrieved < sets[import_set]):
          to_retrieve = min(1000, sets[import_set] - retrieved)
          
          data_query = SolrUtilities.base_query() + '&collection_id=' + collection_id  + '&q=import_classifications:"' + import_set + '"%20AND%20(record_subject:"Array%20ID%2060"%20OR%20record_subject:"Array%20ID%20101")&fl=collection_id,import_set,record_datetime,record_subject,location_name,latitude,longitude,temp_c_avg,temp_avg,hour,jul_day,import_classifications&sort=record_datetime%20asc'
          url = '%s&start=%d&rows=%d' % (data_query, retrieved, to_retrieve)
          print "Solr Query: %s" % url
          
          xmldoc = SolrUtilities.solr_request(url)
          for node in xmldoc.getElementsByTagName('doc'):
            station = None
            dt = None
            temp = None
            jul_day = None
            hour = None
            
            for child in node.childNodes:
              name = child.getAttribute('name')
              if (name == 'temp_c_avg' or name == 'temp_avg'):
                temp = Decimal(child.childNodes[0].nodeValue).quantize(Decimal("0.01"), ROUND_HALF_UP)
              elif (name == 'record_datetime'):
                dt = SolrUtilities.utc_to_est(child.childNodes[0].nodeValue)
              elif (name == 'jul_day'):
                jul_day = child.childNodes[0].nodeValue
              elif (name == 'hour'):
                hour = child.childNodes[0].nodeValue
              elif (name == 'import_classifications'):
                for x in child.childNodes:
                  if x.childNodes[0].nodeValue in stations:
                    station = stations[x.childNodes[0].nodeValue]
                    break
            
            if (station and dt and temp is not None):
              (next_expected_timestamp, last_valid_temp, prev_station, created, updated) = _process_row(cursor, dt, station, float(temp), next_expected_timestamp, last_valid_temp, prev_station)
              created_count = created_count + created
              updated_count = updated_count + updated
              
          xmldoc.unlink()
          retrieved = retrieved + to_retrieve
    
    # Update the last import date
    lid = SolrUtilities.update_last_import_date('respiration')
    cache.set('solr_import_date', lid.strftime('%Y-%m-%d'))
    cache.set('solr_import_time', lid.strftime('%H:%M:%S'))  
    cache.set('solr_created', created_count)
    cache.set('solr_updated', updated_count)

  except Exception,e:
    cache.set('solr_error', str(e)) 
  
  transaction.set_dirty()
  
  cache.set('solr_complete', True)
  
  response = { 'complete': True }
  http_response = HttpResponse(simplejson.dumps(response), mimetype='application/json')
  http_response['Cache-Control']='max-age=0,no-cache,no-store' 
  return http_response

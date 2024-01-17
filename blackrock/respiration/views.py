import codecs
import csv
import datetime
from decimal import Decimal, ROUND_HALF_UP
from json import dumps
import time

from blackrock.blackrock_main.models import LastImportDate
from blackrock.blackrock_main.solr import SolrUtilities
from blackrock.respiration.models import Temperature, StationMapping
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import make_aware
from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from pysolr import Solr


try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


def index(request, admin_msg=""):
    ctx = {'admin_messages': admin_msg}
    return render(request, 'respiration/index.html', ctx)


def leaf(request):
    scenario_options = {
        'name': 'Scenario 1',
        'leafarea': 1,
        'startdate': '1/1',
        'enddate': '12/31',
        'deltat': '',
        'fieldstation': '',
        'year': ''}
    try:
        scenario_options['name'] = request.POST['scenario1-name']
        scenario_options['year'] = request.POST['scenario1-year']
        scenario_options['fieldstation'] = request.POST[
            'scenario1-fieldstation']
        scenario_options['leafarea'] = request.POST['scenario1-leafarea']
        scenario_options['startdate'] = request.POST['scenario1-startdate']
        scenario_options['enddate'] = request.POST['scenario1-enddate']
        scenario_options['deltat'] = request.POST['scenario1-delta-t']
    except MultiValueDictKeyError:
        pass

    specieslist = []
    try:
        specieslist = request.POST['scenario1-species'].split(",")
    except (MultiValueDictKeyError, AttributeError):
        pass

    myspecies = []
    for s in specieslist:
        if (s != ""):
            species = {}
            species['name'] = request.POST[s + '-name']
            species['basetemp'] = request.POST[s + '-base-temp']
            species['E0'] = request.POST[s + '-E0']
            species['R0'] = request.POST[s + '-R0']
            species['percent'] = request.POST[s + '-percent']
            myspecies.append(species)

    return render(request, 'respiration/leaf.html', {
        'numspecies': len(myspecies),
        'specieslist': myspecies,
        'scenario_options': scenario_options})


def forest(request):
    stations = Temperature.objects.values(
        'station').order_by('station').distinct()
    station_names = [item['station'] for item in stations]
    year_options = {}
    for station in station_names:
        years = [item.year for item in Temperature.objects.filter(
            station=station).dates('date', 'year')]
        year_options[station] = str(years)

    # get passed-in defaults
    scenario_options = {
        'name': 'Scenario 1',
        'leafarea': 1,
        'startdate': '1/1',
        'enddate': '12/31',
        'deltat': '0',
        'fieldstation': '', 'year': ''}
    try:
        scenario_options['name'] = request.POST['scenario1-name']
        scenario_options['year'] = request.POST['scenario1-year']
        scenario_options['fieldstation'] = request.POST[
            'scenario1-fieldstation']
        scenario_options['leafarea'] = request.POST['scenario1-leafarea']
        scenario_options['startdate'] = request.POST['scenario1-startdate']
        scenario_options['enddate'] = request.POST['scenario1-enddate']
        scenario_options['deltat'] = request.POST['scenario1-delta-t']
    except MultiValueDictKeyError:
        pass

    specieslist = []
    try:
        specieslist = request.POST['specieslist'].split(",")
    except (MultiValueDictKeyError, AttributeError):
        pass

    myspecies = get_myspecies(specieslist, request)

    return render(request, 'respiration/forest.html', {
        'stations': station_names,
        'years': year_options,
        'numspecies': len(myspecies),
        'specieslist': myspecies,
        'scenario_options': scenario_options,
    })


def get_myspecies(specieslist, request):
    myspecies = []
    for s in specieslist:
        if (s != ""):
            species = {}
            species['basetemp'] = request.POST[s + '-base-temp']
            species['name'] = request.POST[s + '-name']
            species['E0'] = request.POST[s + '-E0']
            species['R0'] = request.POST[s + '-R0']
            try:
                species['percent'] = request.POST[s + '-percent']
            except (MultiValueDictKeyError, KeyError):
                species['percent'] = ''
            myspecies.append(species)
    return myspecies


@csrf_exempt
def getsum(request):
    if request.method != 'POST':
        return HttpResponseRedirect("/respiration/")
    R0 = float(request.POST.get('R0'))
    E0 = float(request.POST.get('E0'))
    T0 = float(request.POST.get('t0'))
    deltaT = 0.0
    try:
        deltaT = float(request.POST.get('delta'))
    except (MultiValueDictKeyError, ValueError):
        deltaT = 0.0

    start = request.POST.get('start')
    startpieces = start.split('/')
    startfinal = datetime.datetime(
        int(startpieces[2]), int(startpieces[0]), int(startpieces[1]))
    end = request.POST.get('end')
    endpieces = end.split('/')
    # we add 1 day so we can do < enddate and include all values for the end
    # date (start and end date are both inclusive)
    endfinal = datetime.datetime(int(endpieces[2]), int(
        endpieces[0]), int(endpieces[1])) + datetime.timedelta(days=1)

    station = request.POST.get('station')
    (total, tm) = Temperature.arrhenius_sum(
        E0, R0, T0, deltaT, startfinal, endfinal, station)
    total_mol = total / 1000000
    json = '{"total": %s}' % round(total_mol, 2)
    return HttpResponse(json, content_type="application/javascript")


_filters = 'station start end year'.split()


def getcsv(request):

    filters = dict((f, request.GET.get(f)) for f in _filters)

    if sum(bool(f) for f in list(filters.values())) != len(filters):
        if not request.user.is_staff:
            msg = "you must provide a station, a year and a season range"
            return HttpResponseForbidden(msg)
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

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename=temperature_readings.csv'
    writer = csv.writer(response)

    # write headers
    headers = ['station', 'year', 'julian day', 'hour',
               'avg temp deg C', 'data source']
    writer.writerow(headers)

    # write data
    temperatures = temperatures.order_by("station", "date")
    for t in temperatures:
        julian_day = (t.date - datetime.datetime(
            year=t.date.year, month=1, day=1)).days + 1
        hour = (t.date.hour + 1) * 100
        year = t.date.year
        row = [t.station, year, julian_day, hour, t.reading, t.data_source]
        writer.writerow(row)

    return response


@user_passes_test(lambda u: u.is_staff)
def loadcsv(request):
    cursor = connection.cursor()

    # if csv file provided, loadcsv
    if request.method != 'POST' or 'csvfile' not in request.FILES:
        return HttpResponse('No csv file specified')

    fh = request.FILES['csvfile']

    # TODO: error checking (correct file type, etc.)

    table = csv.reader(codecs.iterdecode(fh, 'utf-8'))

    headers = next(table)

    (station_idx, year_idx, day_idx, hour_idx, temp_idx,
     response) = header_indices(headers)
    if response is not None:
        return response

    delete_all_temperatures_if_needed(request)

    load_table(table, station_idx, year_idx, day_idx, hour_idx, temp_idx,
               cursor)
    return HttpResponseRedirect('/admin/respiration/temperature')


def header_indices(header):
    indices = dict()
    for i in range(len(header)):
        h = header[i].lower()
        indices[h + "_idx"] = i
        if h == "julian day":
            indices['day_idx'] = i
        if h == "avg temp deg c":
            indices['temp_idx'] = i

    expected = ['station_idx', 'year_idx', 'day_idx', 'hour_idx', 'temp_idx']

    for e in expected:
        if e not in indices:
            expected_str = "station, year, julian day, hour, avg temp deg C"
            msg = "Error: Missing header.  We expect: %s" % expected_str
            return (None, None, None, None, None, HttpResponse(msg))
    return (indices['station_idx'], indices['year_idx'], indices['day_idx'],
            indices['hour_idx'], indices['temp_idx'], None)


def delete_all_temperatures_if_needed(request):
    if request.POST.get('delete') == 'on':
        qs = Temperature.objects.all()
        qs.delete()


def load_table(table, station_idx, year_idx, day_idx, hour_idx, temp_idx,
               cursor):
    next_expected_timestamp = None
    last_valid_temp = None
    prev_station = None

    for row in table:
        station = row[station_idx]
        year = row[year_idx]
        julian_days = row[day_idx]
        hour = row[hour_idx]
        temp = row[temp_idx]
        print(station, year, julian_days, hour, temp)

        # adjust hour from "military" to 0-23, and 2400 becomes 0 of
        # the next day
        normalized_hour = int(hour) // 100 - 1
        # if normalized_hour == 24:
        #  normalized_hour = 0
        # julian_days = int(julian_days) + 1

        delta = datetime.timedelta(days=int(julian_days) - 1)

        # Make this timezone-aware, based on the current timezone (EST).
        dt = datetime.datetime(
            year=int(year),
            month=1,
            day=1,
            hour=normalized_hour
        )

        estdelta = datetime.timedelta(hours=5)
        dt = dt + estdelta
        dt = dt + delta
        print(dt)
        dt = make_aware(dt)
        print(dt)

        (next_expected_timestamp,
         last_valid_temp,
         prev_station,
         created,
         updated) = _process_row(cursor, dt, station, temp,
                                 next_expected_timestamp,
                                 last_valid_temp, prev_station)


def _update_or_insert(cursor, record_datetime, station, temp, data_source):
    created = False
    query = """UPDATE respiration_temperature
               SET reading=%s, data_source=%s where station=%s and date=%s"""
    cursor.execute(query, [str(temp), data_source, station,
                           record_datetime.strftime('%Y-%m-%d %H:%M:%S%z')])
    if cursor.rowcount < 1:
        query = """INSERT into respiration_temperature
                   (station, date, reading, precalc, data_source)
                   values(%s, %s, %s, 1, %s)"""
        cursor.execute(query, [station,
                               record_datetime.strftime('%Y-%m-%d %H:%M:%S%z'),
                               str(temp), data_source])
        created = cursor.rowcount > 0

    return created


def reading_from_temp(last_valid_temp, temp):
    if last_valid_temp is not None:
        return float(last_valid_temp)
    else:
        return float(temp)


def _process_row(cursor, record_datetime, station, temp,
                 next_expected_timestamp, last_valid_temp, prev_station):

    temp = ensure_valid_temp(temp, last_valid_temp, station, prev_station)
    created_count = 0
    updated_count = 0

    # if data is missing, fill in the blanks with the last valid temp
    if (next_expected_timestamp is not None and
            record_datetime != next_expected_timestamp):
        # if dt < expected we just assume it is a duplicate of data we already
        # have
        while (record_datetime > next_expected_timestamp and
               record_datetime.year == next_expected_timestamp.year):
            reading = reading_from_temp(last_valid_temp, temp)
            created = _update_or_insert(
                cursor, next_expected_timestamp, station, reading, 'mock')
            next_expected_timestamp = next_expected_timestamp + \
                datetime.timedelta(hours=1)

            if created:
                created_count = created_count + 1
            else:
                updated_count = updated_count + 1

    if temp != "":
        created = _update_or_insert(
            cursor, record_datetime, station, float(temp), 'original')

        if created:
            created_count = created_count + 1
        else:
            updated_count = updated_count + 1

        next_expected_timestamp = record_datetime + datetime.timedelta(hours=1)

        if (record_datetime.month == 12 and
            record_datetime.day == 31 and
                record_datetime.hour == 23):  # 12/31 11pm (last time of year)
            next_expected_timestamp = None
        last_valid_temp = temp

    return (next_expected_timestamp,
            last_valid_temp,
            station,
            created_count,
            updated_count)


def ensure_valid_temp(temp, last_valid_temp, station, prev_station):
    if temp == "" or float(temp) < -100 or float(temp) > 100:
        if last_valid_temp is not None and station == prev_station:
            temp = last_valid_temp
        else:
            temp = 0
    return temp


def _utc_to_est(date_string):
    try:
        t = time.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        aware = datetime.datetime(
            t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=datetime.timezone(0))
        return aware
    except ValueError:
        return None


def process_station_row(cursor, station, dt, temp, created_count,
                        updated_count, next_expected_timestamp,
                        last_valid_temp, prev_station):
    if (station and dt and temp is not None):
        (next_expected_timestamp,
         last_valid_temp,
         prev_station,
         created,
         updated) = _process_row(cursor, dt, station,
                                 float(temp),
                                 next_expected_timestamp,
                                 last_valid_temp,
                                 prev_station)
        created_count = created_count + created
        updated_count = updated_count + updated
    return (created_count, updated_count, next_expected_timestamp,
            last_valid_temp, prev_station)


@user_passes_test(lambda u: u.is_staff)
def loadsolr(request):
    application = request.POST.get('application', '')
    collection_id = request.POST.get('collection_id', '')
    import_classification = request.POST.get('import_classification', '')
    dt = request.POST.get('last_import_date', '')
    tm = unquote(request.POST.get('last_import_time', '00:00'))
    limit_records = int(request.POST.get('limit_records', '0'))

    solr = Solr(settings.CDRS_SOLR_URL)

    stations = station_mappings_dict()

    created_count = 0
    updated_count = 0
    try:
        cursor = connection.cursor()
        next_expected_timestamp = None
        last_valid_temp = None
        prev_station = None
        retrieved = 0

        last_import_date = LastImportDate.get_last_import_date(
            dt, tm, application)
        options = {'qt': 'forest-data',
                   'collection_id': collection_id,
                   'sort': 'latitude asc,record_datetime asc'}
        q = import_classifications_query(import_classification,
                                         last_import_date)

        record_count = get_record_count(collection_id, import_classification,
                                        last_import_date, limit_records)

        while (retrieved < record_count):
            to_retrieve = min(1000, record_count - retrieved)
            options['start'] = str(retrieved)
            options['rows'] = str(to_retrieve)

            results = solr.search(q, **options)
            for result in results:
                temp = Decimal(str(result['temp_c_avg'])
                               ).quantize(Decimal("0.01"), ROUND_HALF_UP)
                dt = _utc_to_est(result['record_datetime'])

                for x in result['import_classifications']:
                    if x in stations:
                        station = stations[x]
                        break

                (created_count, updated_count, next_expected_timestamp,
                 last_valid_temp, prev_station) = process_station_row(
                     cursor, station, dt, temp, created_count, updated_count,
                     next_expected_timestamp, last_valid_temp, prev_station)

            retrieved = retrieved + to_retrieve

        # Update the last import date
        lid = LastImportDate.update_last_import_date(application)
        cache.set('solr_import_date', lid.strftime('%Y-%m-%d'))
        cache.set('solr_import_time', lid.strftime('%H:%M:%S'))
        cache.set('solr_created', created_count)
        cache.set('solr_updated', updated_count)

    except Exception as e:
        cache.set('solr_error', str(e))

    cache.set('solr_complete', True)

    response = {'complete': True}
    http_response = HttpResponse(
        dumps(response), content_type='application/json')
    http_response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return http_response


def get_record_count(collection_id, import_classification, last_import_date,
                     limit_records):
    record_count = SolrUtilities().get_count_by_lastmodified(
        collection_id, import_classification, last_import_date)
    if limit_records > 0:
        record_count = limit_records
    return record_count


def import_classifications_query(import_classification, last_import_date):
    q = 'import_classifications:"' + import_classification + \
        '" AND (record_subject:"Array ID 60" ' + \
        'OR record_subject:"Array ID 101")'

    if last_import_date:
        utc = last_import_date.astimezone(datetime.timezone(0))
        q += ' AND last_modified:[' + utc.strftime(
            '%Y-%m-%dT%H:%M:%SZ') + ' TO NOW]'
    return q


def station_mappings_dict():
    # stash the station mappings into a python map
    stations = {}
    for sm in StationMapping.objects.all():
        stations[sm.abbreviation] = sm.station
    return stations

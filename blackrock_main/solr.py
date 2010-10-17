from blackrock_main.models import LastImportDate
import datetime, time, pytz, urllib, urllib2
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.conf import settings
from pysolr import Solr, SolrError

class SolrUtilities:
  
  def update_last_import_date(self, application):
    dt = datetime.datetime.now()
    try:
      lid = LastImportDate.objects.get(application=application)
      lid.last_import = dt 
    except LastImportDate.DoesNotExist:
      lid = LastImportDate.objects.create(application=application, last_import=datetime.datetime.now())
    lid.save()
    return dt
  
  def get_last_import_date(self, request, application):
    dt = request.POST.get('last_import_date', '')
    tm =  urllib.unquote(request.POST.get('last_import_time', '00:00'))
    last_import_date = self.string_to_eastern_dst(dt, tm)
    
    if not last_import_date:
      try:
        last_import_date = LastImportDate.objects.get(application=application).last_import
        last_import_date = last_import_date.replace(tzinfo=pytz.timezone('US/Eastern'))
      except LastImportDate.DoesNotExist:
        pass
  
    return last_import_date

  def string_to_eastern_dst(self, date_string, time_string):
    try:
      t = time.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M:%S')
      tz = pytz.timezone('US/Eastern')
      dt = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=tz)
      return dt
    except:
      return None
  
  # Retrieve a list of modified records and row count based on the last time these sets were imported
  def get_count_by_lastmodified(self, collection_id, import_classification, last_import_date):
    solr_conn = Solr(settings.CDRS_SOLR_URL)
    record_count = 0
    options = { 'qt': 'forest-data',
                'collection_id': collection_id,
                'facet': 'true',
                'facet.field': 'import_classifications',
                'facet.mincount': '1',
                'rows': '0',
                'fq': 'import_classifications:"' + import_classification + '"',
                'json.nl': 'map'
               }
    
    if last_import_date:
      utc = last_import_date.astimezone(FixedOffset(0))
      options['fq'] += ' AND last_modified:[' + utc.strftime('%Y-%m-%dT%H:%M:%SZ') + ' TO NOW]'
    
    import_classification = urllib.unquote(import_classification)
    
    results = solr_conn.search('*:*', **options)
    for key, value in results.facets["facet_fields"]["import_classifications"].items():
      if key == import_classification:
        record_count= value
        break
        
    return record_count
from blackrock_main.models import LastImportDate
import datetime, time, pytz, urllib, urllib2
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.conf import settings


class SolrUtilities:
  _solr_base_query = "%s/solr/blackrock/select/?qt=forest-data&" % settings.CDRS_SOLR_URL
  
  def process_request(self, options, processor):
    response = None
    xmldoc = None
    try:
      url = self._solr_base_query + '&'.join([key + "=" + value for key,value in options.items()])
      
      response = urllib2.urlopen(url)
      xmldoc = minidom.parse(response)
      rv = processor(xmldoc)
    finally:
      if xmldoc:
        xmldoc.unlink()
      if response:
        response.close()
    return rv
  
  def make_request(self, options):
    url = self._solr_base_query + '&'.join([key + "=" + value for key,value in options.items()])
      
    response = urllib2.urlopen(url)
    xmldoc = minidom.parse(response)
    response.close()
    return xmldoc
  
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
    record_count = 0
    options = { 'collection_id': collection_id,
                'facet': 'true',
                'facet.field': 'import_classifications',
                'facet.mincount': '1',
                'fq': 'import_classifications:"' + import_classification + '"',
                'rows': '0',
                'q': '*:*',
               }
#    count_query = self._solr_base_query + 'collection_id=' + collection_id + '&facet=true&facet.field=import_classifications&rows=0'
#    count_query = count_query + '&q=*:*&facet.mincount=1&fq=import_classifications:"' + import_classification + '"'
    
    if last_import_date:
      utc = last_import_date.astimezone(FixedOffset(0))
      options['fq'] += '%20AND%20last_modified:[' + utc.strftime('%Y-%m-%dT%H:%M:%SZ') + '%20TO%20NOW]'
    
    import_classification = urllib.unquote(import_classification)
    
    xmldoc = self.make_request(options)
    for node in xmldoc.getElementsByTagName('int'):
      if node.hasAttribute('name') and int(node.childNodes[0].nodeValue) > 0 and node.getAttribute('name') == import_classification:
        record_count = int(node.childNodes[0].nodeValue)
        break
    xmldoc.unlink()

    return record_count
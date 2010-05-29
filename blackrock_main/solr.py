from blackrock_main.models import LastImportDate
import datetime, time, pytz, urllib, urllib2
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.utils.http import urlquote

class SolrUtilities:
  _solr_base_query = 'http://seasnail.cc.columbia.edu:8181/solr/blackrock/select/?qt=forest-data&'
  
  @classmethod
  def update_last_import_date(self, application):
    dt = datetime.datetime.now()
    try:
      lid = LastImportDate.objects.get(application=application)
      lid.last_import = dt 
    except LastImportDate.DoesNotExist:
      lid = LastImportDate.objects.create(application=application, last_import=datetime.datetime.now())
    lid.save()
    return dt
  
  @classmethod
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

  @classmethod
  def string_to_eastern_dst(self, date_string, time_string):
    try:
      t = time.strptime(date_string + ' ' + time_string, '%Y-%m-%d %H:%M:%S')
      tz = pytz.timezone('US/Eastern')
      dt = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=tz)
      return dt
    except:
      return None
   
  # Convert the UTC solr datetime string to an EST datetime object
  @classmethod
  def utc_to_est(self, date_string):
    try:
      t = time.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
      utc = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=FixedOffset(0))
      utc = utc - datetime.timedelta(hours=1) # Subtract an hour to account for raw data 1-24 timespan
      est = utc.astimezone(FixedOffset(-300)) #UTC -5 hours. Solr dates are always EST and do not take dst into account
      return est
    except:
      return None
    
  @classmethod
  def solr_request(self, url):
    response = urllib2.urlopen(url)
    xmldoc = minidom.parse(response)
    response.close()
    return xmldoc
  
  # Retrieve a list of modified import sets and row count based on the last time these sets were imported
  @classmethod
  def get_importsets_by_lastmodified(self, collection_id, import_set_type, last_import_date, import_set):
    sets = {}
    
    count_query = self._solr_base_query + 'collection_id=' + collection_id + '&facet=true&facet.field=import_set&rows=0'
    count_query = count_query + '&q=import_set_type:"' + import_set_type + '"'
    
    if last_import_date:
      utc = last_import_date.astimezone(FixedOffset(0))
      count_query = count_query + '%20AND%20last_modified:[' + utc.strftime('%Y-%m-%dT%H:%M:%SZ') + '%20TO%20NOW]'
    if len(import_set) > 0:
      count_query = count_query + '%20AND%20import_set:"' + import_set + '"'
      
    xmldoc = self.solr_request(count_query)
    for node in xmldoc.getElementsByTagName('int'):
      if node.hasAttribute('name') and int(node.childNodes[0].nodeValue) > 0:
        sets[node.getAttribute('name')] = int(node.childNodes[0].nodeValue)
    xmldoc.unlink()
    
    return sets
  
  @classmethod
  def base_query(self):
    return self._solr_base_query
from blackrock_main.models import LastImportDate
import datetime, time, pytz, urllib, urllib2
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset

class SolrUtilities:
  @classmethod
  def update_last_import_date(self, application):
    try:
      lid = LastImportDate.objects.get(application=application)
      lid.last_import = datetime.datetime.now()
    except LastImportDate.DoesNotExist:
      lid = LastImportDate.objects.create(application=application, last_import=datetime.datetime.now())
    lid.save()

  
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
      est = utc.astimezone(FixedOffset(-300)) # subtract 5 hours
      return est
    except:
      return None
    
  @classmethod
  def solr_request(self, url):
    response = urllib2.urlopen(url)
    xmldoc = minidom.parse(response)
    response.close()
    return xmldoc
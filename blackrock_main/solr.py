from blackrock_main.models import LastImportDate
import datetime, time, pytz, urllib, urllib2
from xml.dom import minidom
from django.utils.tzinfo import FixedOffset
from django.conf import settings
from pysolr import Solr, SolrError

class SolrUtilities:
  # Retrieve a list of modified records and row count based on the last time these sets were imported
  def get_count_by_lastmodified(self, collection_id, import_classification, last_import_date):
    solr_conn = Solr(settings.CDRS_SOLR_URL)
    record_count = 0
    options = { 'qt': 'forest-data',
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
    
    collections = urllib.unquote(collection_id).split(",")
    for c in collections:
      # Get list of datasets in each collection id
      options['collection_id'] = c

      results = solr_conn.search('*:*', **options)
      for key, value in results.facets["facet_fields"]["import_classifications"].items():
        if key == import_classification:
          record_count += value
          break
        
    return record_count
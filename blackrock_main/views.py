from blackrock_main.models import LastImportDate
from blackrock_main.solr import SolrUtilities
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import simplejson
import urllib


# returns important setting information for all web pages.
def django_settings(request):
    whitelist = ['DATABASE_HOST',
                 'DATABASE_NAME',
                 'GOOGLE_MAP_API']

    rv = {'settings': dict([(k, getattr(settings, k, None))
                            for k in whitelist])}

    return rv


@user_passes_test(lambda u: u.is_staff)
def loadsolr_poll(request):
    response = {'solr_complete': False}
    if 'solr_complete' in cache:
        response['solr_complete'] = True
        cache.delete('solr_complete')

        if 'solr_error' in cache:
            response['solr_error'] = cache.get('solr_error')
            cache.delete('solr_error')

        if 'solr_created' in cache:
            response['solr_created'] = cache.get('solr_created')
            cache.delete('solr_created')

        if 'solr_updated' in cache:
            response['solr_updated'] = cache.get('solr_updated')
            cache.delete('solr_updated')

        if 'solr_import_date' in cache:
            response['solr_import_date'] = cache.get('solr_import_date')
            response['solr_import_time'] = cache.get('solr_import_time')
            cache.delete('solr_import_date')
            cache.delete('solr_import_time')

    http_response = HttpResponse(
        simplejson.dumps(response), mimetype='application/json')
    http_response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return http_response


@user_passes_test(lambda u: u.is_staff)
def previewsolr(request):
    response = {}
    solr = SolrUtilities()

    application = request.POST.get('application', '')
    collection_id = request.POST.get('collection_id', '')
    import_classification = request.POST.get('import_classification', '')
    dt = request.POST.get('last_import_date', '')
    tm = urllib.unquote(request.POST.get('last_import_time', '00:00'))

    last_import_date = LastImportDate.get_last_import_date(dt, tm, application)
    response['record_count'] = solr.get_count_by_lastmodified(
        collection_id, import_classification, last_import_date)

    if last_import_date:
        response['last_import_date'] = last_import_date.strftime('%Y-%m-%d')
        response['last_import_time'] = last_import_date.strftime('%H:%M:%S')

    http_response = HttpResponse(
        simplejson.dumps(response), mimetype='application/json')
    http_response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return http_response

from datetime import date, timezone
from decimal import Decimal
import io
import json
import re
import sys
from time import strptime

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D  # D is a shortcut for Distance
from django.core import management
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import DateField
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import TemplateView
import django_databrowse
from pagetree.models import Hierarchy
from pysolr import Solr, SolrError

from blackrock.blackrock_main.models import LastImportDate
from blackrock.blackrock_main.solr import SolrUtilities
from blackrock.portal.models import Location, DataSet, Audience, \
    get_all_related_objects


try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if isinstance(items, type({})):
                return render(request, self.template_name,
                              items, {})
            else:
                return items

        return rendered_func


class PortalPageView(TemplateView):
    template_name = 'portal/page.html'

    def get_context_data(self, **kwargs):
        ctx = TemplateView.get_context_data(self, **kwargs)
        path = kwargs.get('path', '')

        h = Hierarchy.get_hierarchy('main')
        current_root = h.get_section_from_path(path)
        section = h.get_first_leaf(current_root)
        ancestors = section.get_ancestors()

        module = None
        if not section.is_root() and len(ancestors) > 1:
            module = ancestors[1]

        asset_type = self.request.GET.get('type', None)
        asset_id = self.request.GET.get('id', None)

        root = None
        if len(ancestors) > 0:
            root = ancestors[0]

        ctx['section'] = section
        ctx['module'] = module
        ctx['root'] = root

        if asset_type and asset_id:
            try:
                model = apps.get_model("portal", asset_type)
                ctx['selected'] = model.objects.get(id=asset_id)
            except (ObjectDoesNotExist, LookupError, ValueError):
                msg = "We were unable to locate a <b>%s</b> at this address."
                ctx['error'] = msg % (asset_type)

        return ctx


def portal_databrowse(request, url):
    url = url.rstrip('/')  # Trim trailing slash, if it exists.

    if 'objects' in url:
        return django_databrowse.site.root(request, url)
    else:
        return HttpResponseRedirect(reverse('portal-search'))


@rendered_with('portal/nearby.html')
def nearby(request, latitude, longitude):
    # loc = Location.objects.get(name="Tamarack Pond") latitude =
    # 41.3947630000 / longitude = -74.0251920000
    point = 'POINT(%s %s)' % (latitude, longitude)
    pnt = fromstr(point, srid=4326)

    qs = Location.objects.filter(latlong__distance_lte=(
        pnt, D(mi=.15))).annotate(distance=Distance('latlong', pnt))

    a = []
    for loc in qs:
        all_related = get_all_related_objects(loc)
        for obj in all_related:
            for instance in getattr(loc, obj.get_accessor_name()).all():
                if len(a) < 10:
                    a.append(instance)

    return dict(latitude=latitude,
                longitude=longitude,
                results=a,
                count=len(a))


def process_datasets(xmldoc):
    datasets = []
    for node in xmldoc.getElementsByTagName('int'):
        if node.hasAttribute('name'):
            datasets.append(node.getAttribute('name'))

    return datasets


def process_date(date_string):
    if re.match(r'\d\d\d\d-\d\d?-\d\d?', date_string):
        t = strptime(date_string, '%Y-%m-%d')
    elif re.match(r'\d\d\d\d-\d\d?', date_string):
        t = strptime(date_string, '%Y-%m')
    elif re.match(r'\d\d\d\d', date_string):
        t = strptime(date_string, '%Y')

    if t:
        return date(t[0], t[1], t[2])

    return None


_dataset_field_map = {
    'dataset_id': 'blackrock_id',
    'title': 'name',
    'abstract': 'description',
    'field_study_data_collection_start_date': 'collection_start_date',
    'field_study_data_collection_end_date': 'collection_end_date',
    'restriction_on_access': 'rights_type',
    'related_files': 'url',
    'educational_data_files': 'url',
    'lead_investigators': 'person',
    'other_investigators': 'person',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'species': 'facet',
    'discipline': 'facet',
    'scientific_study_type': 'facet',
    'keywords': 'tag'
}


def _is_dirty(original_state, new_state):
    for key, value in original_state.items():
        if new_state[key] is not None and value != new_state[key]:
            return True
    return False


def process_location(values):
    location = None
    if 'latitude' in values and 'longitude' in values:
        lat = Decimal(values['latitude'][0].replace('+', ''))
        lng = Decimal(values['longitude'][0])
        location, created = Location.objects.get_or_create(
            name=values['name'][0], latitude=lat, longitude=lng)
    return location


def process_fieldnames(result):
    values = {}
    for key, value in list(result.items()):
        if value and key in list(_dataset_field_map.keys()):
            fieldname = _dataset_field_map[key]
            if fieldname not in values:
                values[fieldname] = []
            if isinstance(value, type(list())):
                values[fieldname].extend(value)
            else:
                values[fieldname].append(value)
    return values


def save_if_created(created, dataset):
    if created:
        dataset.save()


def process_metadata(result):
    created = False
    dataset = None

    try:
        the_id = result['dataset_id']
        dataset = DataSet.objects.get(blackrock_id=the_id)
    except DataSet.DoesNotExist:
        dataset = DataSet()
        created = True

    original_state = dict(dataset.__dict__)

    values = process_fieldnames(result)

    dataset = process_dataset_meta_fields(dataset, values)

    dataset.location = process_location(values)
    save_if_created(created, dataset)

    for field in dataset._meta.many_to_many:
        if field.name in list(values.keys()):
            related_model = apps.et_model("portal", field.name)
            for v in values[field.name]:
                if field.name == 'url':
                    v = settings.CDRS_SOLR_FILEURL + v
                related_obj, temp_created = \
                    related_model.objects.get_or_create(name=v.strip())
                dataset.__getattribute__(field.name).add(related_obj)

    dataset.audience.add(Audience.objects.get(name='Research'))

    save_if_dirty(original_state, dataset)

    return created


def save_if_dirty(original_state, dataset):
    if _is_dirty(original_state, dict(dataset.__dict__)):
        dataset.save()


def process_dataset_meta_fields(dataset, values):
    for field in dataset._meta.fields:
        if field.name in list(values.keys()):
            if isinstance(field, DateField):
                value = process_date(values[field.name][0])
            else:
                value = values[field.name][0]
            dataset.__setattr__(field.name, value)
    return dataset


@user_passes_test(lambda u: u.is_staff)
def admin_cdrs_import(request):
    if (request.method != 'POST'):
        return render(request, 'portal/admin_cdrs.html', {})

    created = 0
    updated = 0
    solr = Solr(settings.CDRS_SOLR_URL)

    application = request.POST.get('application', '')
    collection_id = request.POST.get('collection_id', '')
    import_classification = request.POST.get('import_classification', '')
    dt = request.POST.get('last_import_date', '')
    tm = unquote(request.POST.get('last_import_time', '00:00'))
    options = {'qt': 'forest-data'}
    last_import_date = LastImportDate.get_last_import_date(dt, tm, application)

    q = import_classification_query(import_classification, last_import_date)

    try:
        collections = unquote(collection_id).split(",")
        for c in collections:
            # Get list of datasets in each collection id
            created, updated = get_collection_datasets(
                c, solr, options, q, import_classification, last_import_date,
                created, updated)

        # Update the last import date
        lid = LastImportDate.update_last_import_date(application)
        cache.set('solr_import_date', lid.strftime('%Y-%m-%d'))
        cache.set('solr_import_time', lid.strftime('%H:%M:%S'))
        cache.set('solr_created', created)
        cache.set('solr_updated', updated)
    except Exception as e:
        cache.set('solr_error', str(e))

    cache.set('solr_complete', True)

    response = {'complete': True}
    http_response = HttpResponse(
        json.dumps(response), content_type='application/json')
    http_response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return http_response


def get_collection_datasets(c, solr, options, q, import_classification,
                            last_import_date, created, updated):
    record_count = SolrUtilities().get_count_by_lastmodified(
        c, import_classification, last_import_date)
    retrieved = 0
    while (retrieved < record_count):
        to_retrieve = min(1000, record_count - retrieved)
        options['collection_id'] = c
        options['start'] = str(retrieved)
        options['rows'] = str(to_retrieve)

        results = solr.search(q, **options)
        for result in results:
            if 'dataset_id' in result:
                if process_metadata(result):
                    created += 1
                else:
                    updated += 1

        retrieved = retrieved + to_retrieve
    return created, updated


def import_classification_query(import_classification, last_import_date):
    q = 'import_classifications:"' + import_classification + '"'

    if last_import_date:
        utc = last_import_date.astimezone(timezone(0))
        q += ' AND last_modified:[' + utc.strftime(
            '%Y-%m-%dT%H:%M:%SZ') + ' TO NOW]'
    return q


@user_passes_test(lambda u: u.is_staff)
def admin_rebuild_index(request):
    ctx = {'server': settings.HAYSTACK_CONNECTIONS['default']['URL']}

    if (request.method == 'POST'):
        sys.stdout = the_buffer = io.StringIO()
        management.call_command('rebuild_index', interactive=False)
        sys.stdout = sys.__stdout__
        ctx['results'] = the_buffer.getvalue().split('\n')[1:-2]

    return render(request, 'portal/admin_solr.html', ctx)


def admin_readercycle(request):
    solr_url = settings.HAYSTACK_CONNECTIONS['default']['URL']
    try:
        solr = Solr(solr_url)
        solr.readercycle()
        return HttpResponse("Cycled")
    except (IOError, SolrError) as e:
        msg = "Failed to cycle Solr %s %s" % (solr_url, e)
        return HttpResponse(msg)

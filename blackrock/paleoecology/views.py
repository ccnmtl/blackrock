from blackrock.paleoecology.models import PollenType, PollenSample, CoreSample
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from pysolr import Solr
import csv
import re
import unicodedata
import simplejson as json


def index(request, admin_msg=""):
    ctx = RequestContext(request, {'admin_messages': admin_msg})
    return render_to_response('paleoecology/index.html', context_instance=ctx)


def identification(request):
    return render_to_response('paleoecology/identification.html')


def explore(request):
    samples = CoreSample.objects.all().order_by('depth')
    # TODO figure out from data
    interval = 2.5  # cm
    highest = 1070 + 2.5  # cm
    intervals = [int(n * interval) for n in range(int(highest / interval))]

    cores = [{'depth': float(sample.depth),
              'radiocarbon_years': sample.radiocarbon_years}
             for sample in samples]

    samples = [float(sample.depth) for sample in samples]

    return render_to_response('paleoecology/core-explore.html',
                              {'samples': samples,
                               'cores': cores,
                               'intervals': intervals})


def getpercents(request):
    depth = request.REQUEST['depth']
    samples = PollenSample.objects.filter(core_sample__depth=depth)
    samples = samples.filter(percentage__isnull=False)
    samples.exclude(percentage=0).order_by('pollen__name')
    results = [(s.pollen.display_name,
                str(s.percentage),
                int(s.count or 0)) for s in samples]
    names = []
    percents = []
    counts = []
    otherpct = 100
    try:
        names, percents, counts = zip(*results)
        otherpct = 100 - sum([float(i) for i in percents])
    except:
        pass
    results = {'depth': depth, 'pollen': names, 'percents': percents,
               'counts': counts, 'other': otherpct}

    return HttpResponse(json.dumps(results), mimetype="application/javascript")


@user_passes_test(lambda u: u.is_staff)
def getcsv(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=coresamples.csv'
    csv.writer(response)
    return response


@user_passes_test(lambda u: u.is_staff)
def loadcounts(request):
    return loadcsv(request, "counts")


@user_passes_test(lambda u: u.is_staff)
def loadpercents(request):
    return loadcsv(request, "percents")


@user_passes_test(lambda u: u.is_staff)
def loadcsv(request, type):
    # if csv file provided, load
    if request.method == 'POST':

        try:
            fh = request.FILES['csvfile']
        except:
            return HttpResponseRedirect("/paleoecology/")

        if file == '':
            # TODO: error checking (correct file type, etc.)
            return HttpResponseRedirect("/paleoecology/")

        table = csv.reader(fh)
        headers = table.next()

        pines = ["Pinus subg. Pinus", "Pinus subg. Strobus", "Pinus undiff."]
        asteraceae = ["Asteraceae subf. Asteroideae undiff.",
                      "Asteraceae subf. Cichorioideae",
                      "Ambrosia", "Artemisia"]

        for row in table:
            depth = row[0]
            (core, created) = CoreSample.objects.get_or_create(depth=depth)

            for i in range(len(row)):
                if i == 0:
                    continue  # skip row[0], which is the depth

                # skip row[1] in percentages, which is the carbon age
                if i == 1 and type == "percents":
                    continue

                pollen_name = headers[i].strip()
                (t, created) = \
                    PollenType.objects.get_or_create(name=pollen_name)
                (p, created) = \
                    PollenSample.objects.get_or_create(core_sample=core,
                                                       pollen=t)

                if type == "counts":
                    p.count = row[i]
                else:
                    p.percentage = row[i]
                p.save()

                # hack to fix Pinus and Asteraceae counts
                if type == "counts":
                    if pollen_name in pines:
                        (second, created) = \
                            PollenType.objects.get_or_create(name="Pinus")
                        (p, created) = \
                            PollenSample.objects.get_or_create(
                                core_sample=core,
                                pollen=second)
                        if created:
                            p.display_name = "Pinus (Pine)"
                        p.count = (p.count or 0) + int(row[i])
                        p.save()

                    if pollen_name in asteraceae:
                        (second, created) = \
                            PollenType.objects.get_or_create(name="Asteraceae")
                        (p, created) = \
                            PollenSample.objects.get_or_create(
                                core_sample=core,
                                pollen=second)
                        if created:
                            p.display_name = 'Asteraceae (Ragweed & herbs)'
                        p.count = (p.count or 0) + int(row[i])
                        p.save()

        admin_msg = "Successfully imported data."

        return index(request, admin_msg)

    return HttpResponseRedirect("/paleoecology/")

_sets = ['Pollen Types',
         'Raw Counts of 65 Pollen Types',
         'Percentages of 15 Pollen Types']


@user_passes_test(lambda u: u.is_staff)
def loadsolr(request):
    collection_id = request.POST.get('collection_id', '')
    import_classification = request.POST.get('import_classification', '')
    solr = Solr(settings.CDRS_SOLR_URL)

    created_count = 0
    updated_count = 0

    PollenSample.objects.all().delete()

    options = {'qt': 'forest-data',
               'collection_id': collection_id,
               'rows': '1000',
               'json.nl': 'map'
               }

    try:
        set = "Pollen Types"
        results = solr.search('import_classifications:("' +
                              import_classification + '" AND "' + set + '")',
                              **options)
        created, updated = process_pollen_types(results)
        created_count += created
        updated_count += updated

        set = 'Raw Counts of 65 Pollen Types'
        results = solr.search('import_classifications:("' +
                              import_classification + '" AND "' + set + '")',
                              **options)
        created, updated = _process_samples(results, "count")
        created_count += created
        updated_count += updated

        set = 'Percentages of 15 Pollen Types'
        results = solr.search('import_classifications:("' +
                              import_classification + '" AND "' + set + '")',
                              **options)
        created, updated = _process_samples(results, "percentage")
        created_count = created_count + created
        updated_count = updated_count + updated

        cache.set('solr_created', created_count)
        cache.set('solr_updated', updated_count)
    except Exception, e:
        cache.set('solr_error', str(e))

    cache.set('solr_complete', True)

    response = {'complete': True}
    http_response = HttpResponse(json.dumps(response),
                                 mimetype='application/json')
    http_response['Cache-Control'] = 'max-age=0,no-cache,no-store'
    return http_response


def process_pollen_types(results):
    created_count = 0
    updated_count = 0

    for result in results:
        plant_name = _normalize_pollen_name(result['plant_name'])
        plant_type = result['plant_type_code']

        pt, created = _get_or_create_pollen_type(plant_name, plant_type)

        if created:
            created_count += 1
        else:
            updated_count += 1

    # a few manual entries for summary purposes
    _get_or_create_pollen_type("Pinus", "A", "Pinus (Pine)")
    _get_or_create_pollen_type("Asteraceae", "B",
                               "Asteraceae (Ragweed & herbs)")

    return created_count, updated_count


def _process_samples(results, fieldname):
    created_count = 0
    updated_count = 0
    exceptions = ['longitude', 'latitude', 'depth_cm', 'workbook_row_number']

    pinus_pollen = PollenType.objects.get(name='Pinus')
    asteraceae_pollen = PollenType.objects.get(name='Asteraceae')

    pines = ["pinus subg pinus", "pinus subg strobus", "pinus undiff"]
    asteraceae = ["asteraceae subf asteroideae undiff",
                  "asteraceae subf cichorioideae", "ambrosia", "artemisia"]

    for result in results:
        subj = result['record_subject']
        core_sample, created = _get_or_create_core_sample(subj)
        for name, value in result.items():
            if name not in exceptions and type(value) == type(float()):
                # solr names for count/percentages come in lowercase
                # with underscores replacing spaces
                pollen_name = _normalize_pollen_name(name)
                pollen_type = PollenType.objects.get(name__iexact=pollen_name)
                value = round(value, 2)

                pollen_count, created = \
                    _update_or_create_pollen_sample(pollen_type,
                                                    core_sample,
                                                    fieldname,
                                                    value)
                if created:
                    created_count += 1
                else:
                    updated_count += 1

                if fieldname == 'count':
                    if pollen_name.lower() in pines:
                        _update_or_create_pollen_sample(pinus_pollen,
                                                        core_sample,
                                                        fieldname,
                                                        value,
                                                        summarize=True)
                    elif pollen_name.lower() in asteraceae:
                        _update_or_create_pollen_sample(asteraceae_pollen,
                                                        core_sample,
                                                        fieldname,
                                                        value,
                                                        summarize=True)

    return created_count, updated_count


def _get_or_create_pollen_type(name, type, display_name=""):
    pt, created = PollenType.objects.get_or_create(name__iexact=name)

    if created:
            pt.name = name

    if len(type) == 1:  # Organic Matter's type is gibberish
        pt.type = type

    if len(display_name) > 0:
        pt.display_name = display_name

    pt.save()

    return pt, created


# Format of record_subject is Depth of XX cm. Parse out the XX,
# find or create a core sample. Continue.
def _get_or_create_core_sample(depth):
    d = re.search('\d+.\d+', depth) or re.search('\d+', depth)
    return CoreSample.objects.get_or_create(depth=d.group(0))


def _update_or_create_pollen_sample(pollen_type,
                                    core_sample,
                                    fieldname,
                                    value,
                                    summarize=False):

    ps, created = PollenSample.objects.get_or_create(pollen=pollen_type,
                                                     core_sample=core_sample)

    value = float(value)
    if summarize:
        oldval = ps.__getattribute__(fieldname)
        if oldval:
            value += float(oldval)
    ps.__setattr__(fieldname, str(value))

    ps.save()

    return ps, created


def _normalize_pollen_name(pollen_name):
    translate = {
        'poaceae': 'Gramineae',
        'organic matter (percent dry mass)': 'Organic matter',
        'o/c': 'Ostrya_Carpinus',
        'ostrya_carpinus': 'Ostrya_Carpinus',
        'asteraceae (incl ragweed)': 'Asteraceae',
        'birch': 'Betula',
        'spruce': 'Picea',
        'castanea': 'Castanea dentata',
        'tsuga': 'Tsuga canadensis',
        'fagus': 'Fagus grandifolia'
    }

    if pollen_name.lower() in translate:
        return translate[pollen_name.lower()]
    else:
        pollen_name = pollen_name.strip().replace('_', ' ')
        pollen_name = pollen_name.replace('.', '')
        pollen_name = pollen_name.replace('(', '')
        pollen_name = pollen_name.replace(')', '')
        pollen_name = pollen_name.replace('/', '_')
        pollen_name = unicode(pollen_name)
        pollen_name = unicodedata.normalize('NFKD', pollen_name)
          # remove any special characters
        pollen_name = pollen_name.encode('ascii', 'ignore')
        return pollen_name

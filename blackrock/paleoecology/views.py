from blackrock.paleoecology.models import PollenSample, CoreSample
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
import json


def index(request, admin_msg=""):
    ctx = RequestContext(request, {'admin_messages': admin_msg})
    return render(request, 'paleoecology/index.html', context_instance=ctx)


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

    return render(request, 'paleoecology/core-explore.html',
                  {'samples': samples,
                   'cores': cores,
                   'intervals': intervals})


def getpercents(request):
    depth = request.GET.get('depth', None)
    if not depth:
        depth = request.POST.get('depth', None)

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
    except ValueError:
        pass

    results = {'depth': depth, 'pollen': names, 'percents': percents,
               'counts': counts, 'other': otherpct}

    return HttpResponse(json.dumps(results),
                        content_type="application/javascript")

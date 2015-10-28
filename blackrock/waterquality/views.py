from annoying.decorators import render_to
from .models import Series, LimitedSeries, LimitedSeriesPair
from .models import LimitedSeriesGroup
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import math
from django.conf import settings
import re


@render_to('waterquality/index.html')
def index(request):
    return dict()


@render_to('waterquality/teaching.html')
def teaching(request):
    return dict()


def parse_date(s):
    (year, month, day) = s.split("-")
    return datetime(int(year), int(month), int(day))


def get_start_or_error(start):
    if not start:
        return get_default_start(), None
    try:
        return parse_date(start), None
    except:
        return None, "invalid start date: %s" % start


def get_end_or_error(end):
    if not end:
        return get_default_end(), None
    try:
        return parse_date(end), None
    except:
        return None, "invalid end date: %s" % end


def get_lines(request):
    lines = []
    # iterating over QueryDict for keys starting with line_value
    # and using v to get value
    for k in request.GET.keys():
        if k.startswith("line_value_"):
            v = request.GET.get(k, '')  # why ''?
            if v:
                n = k[len("line_value_"):]
                l = request.GET.get("line_label_%s" % n)
                lines.append(dict(label=l, value=v, n=int(n)))
    return lines


def get_all_series(series_ids):
    all_series = []
    for series in Series.objects.all():
        if str(series.id) in series_ids:
            series.selected = True
        all_series.append(series)
    return all_series


@render_to('waterquality/graphing_tool.html')
def graphing_tool(request):
    data = dict()
    graph_type = request.GET.get('type', None)

    start, err = get_start_or_error(request.GET.get('start', None))
    if err:
        data['error'] = err
        return data

    end, err = get_end_or_error(request.GET.get('end', None))
    if err:
        data['error'] = err
        return data

    data["start"] = start
    data["end"] = end

    if graph_type == 'time-series' or graph_type == 'scatter-plot':
        data["lines"] = get_lines(request)

    if graph_type == 'time-series':
        series_ids = request.GET.getlist('series')
        datasets = []
        data_count = 0
        for sid in series_ids:
            series = get_object_or_404(Series, id=sid)
            d = series.range_data(start, end, max_points=50000)
            data_count += len(d)
            if data_count < settings.MAX_DATA_COUNT:
                datasets.append(
                    dict(
                        series=series,
                        lseries=LimitedSeries(
                            series=series, start=start, end=end),
                        data=d)
                )
            else:
                data['too_much_data'] = True

        data["datasets"] = datasets
        data['all_series'] = get_all_series(series_ids)
        data['show_graph'] = True

    if graph_type == 'box-plot':
        series_ids = request.GET.getlist('series')
        datasets = []
        for sid in series_ids:
            series = get_object_or_404(Series, id=sid)
            lseries = LimitedSeries(series=series, start=start, end=end)
            datasets.append(lseries)

        data["datasets"] = datasets
        data["lsg"] = LimitedSeriesGroup(series=datasets)
        data['all_series'] = get_all_series(series_ids)
        data['show_graph'] = False
        data['show_box_plot'] = len(datasets) > 0

        if len(series_ids) == 2:
            # we can do a t-test
            s1 = get_object_or_404(Series, id=series_ids[0])
            s2 = get_object_or_404(Series, id=series_ids[1])
            ls1 = LimitedSeries(series=s1, start=start, end=end)
            ls2 = LimitedSeries(series=s2, start=start, end=end)
            m1 = ls1.mean()
            m2 = ls2.mean()
            sd1 = ls1.stddev()
            sd2 = ls2.stddev()
            n1 = ls1.count()
            n2 = ls2.count()
            numerator = (m1 - m2)
            denominator = math.sqrt((sd1 / float(n1)) + (sd2 / float(n2)))
            data['ttest'] = float(numerator) / float(denominator)
            data['show_ttest'] = True

    if graph_type == 'scatter-plot':
        independent = request.GET.get('independent', None)
        dependent = request.GET.get('dependent', None)
        skip_zeroes = request.GET.get('skip_zeroes', None)

        if independent and dependent:
            ind_series = get_object_or_404(Series, id=independent)
            dep_series = get_object_or_404(Series, id=dependent)

            data["datasets"] = [
                dict(
                    series=ind_series,
                    lseries=LimitedSeries(
                        series=ind_series, start=start, end=end)),
                dict(
                    series=dep_series,
                    lseries=LimitedSeries(
                        series=dep_series, start=start, end=end))
            ]
            ind_data = ind_series.range_data(start, end, max_points=50000)
            dep_data = dep_series.range_data(start, end, max_points=50000)
            data['lseriesp'] = LimitedSeriesPair(independent=ind_series,
                                                 dependent=dep_series,
                                                 start=start,
                                                 end=end,
                                                 skip_zeroes=skip_zeroes)
            data["data"] = zip(ind_data, dep_data)
            if skip_zeroes:
                newdata = []
                for d in data["data"]:
                    if d[0] == 0 or d[1] == 0 or d[0] == 0.0 or d[1] == 0.0:
                        continue
                    newdata.append(d)
                data["data"] = newdata
            data["independent"] = ind_series
            data["dependent"] = dep_series
            data["skip_zeroes"] = skip_zeroes

        all_series = []
        for series in Series.objects.all():
            if str(series.id) == independent:
                series.independent = True
            if str(series.id) == dependent:
                series.dependent = True
            all_series.append(series)
        data['show_graph'] = True
        data['all_series'] = all_series

    t = end - start
    data['seconds'] = t.seconds
    data['days'] = t.days
    data['type'] = graph_type
    data['graph_title'] = request.GET.get('title', "")[:50]
    p = re.compile(r'\W+')
    data['filename_base'] = p.sub('_', data['graph_title'])
    return data


@render_to('waterquality/browse.html')
def browse(request):
    return dict(series=Series.objects.all())


@render_to('waterquality/series.html')
def series(request, id):
    series = get_object_or_404(Series, id=id)
    start = request.GET.get('start', False)
    if not start:
        start = series.start().timestamp
    end = request.GET.get('end', False)
    if not end:
        end = series.end().timestamp

    lseries = LimitedSeries(series=series, start=start, end=end)

    return dict(series=series, lseries=lseries)


@render_to('waterquality/series_all.html')
def series_all(request, id):
    series = get_object_or_404(Series, id=id)
    return dict(series=series)


@render_to('waterquality/series_verify.html')
def series_verify(request, id):
    series = get_object_or_404(Series, id=id)
    start_date = series.row_set.all()[0].timestamp
    end_date = series.row_set.all().order_by("-timestamp")[0].timestamp
    step_date = start_date
    d = timedelta(hours=1)
    missing = 0
    found = 0
    while step_date < end_date:
        r = series.row_set.filter(timestamp=step_date)
        if r.count() == 0:
            missing += 1
        else:
            found += 1
        step_date = step_date + d

    return dict(
        missing=missing, found=found,
        total=series.row_set.all().count())


def get_default_start():
    return Series.objects.all()[0].row_set.all()[0].timestamp


def get_default_end():
    return datetime(year=2009, month=12, day=31)

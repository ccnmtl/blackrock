from models import Series,Row,LimitedSeries, LimitedSeriesPair, LimitedSeriesGroup
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from datetime import datetime, timedelta

class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items

        return rendered_func

@rendered_with('waterquality/index.html')
def index(request):
    data = dict()
    start = request.GET.get('start',None)
    end = request.GET.get('end',None)

    graph_type = request.GET.get('type',None)

    if not start:
        start = get_default_start()
    else:
        (year,month,day) = start.split("-")
        start = datetime(int(year),int(month),int(day))

    if not end:
        end = get_default_end()
    else:
        (year,month,day) = end.split("-")
        end = datetime(int(year),int(month),int(day))

    data["start"] = start
    data["end"] = end

    if graph_type == 'time-series':
        series_ids = request.GET.getlist('series')
        datasets = []
        for sid in series_ids:
            series = get_object_or_404(Series,id=sid)
            datasets.append(
                dict(series=series,
                     lseries=LimitedSeries(series=series,start=start,end=end),
                     data=series.range_data(start,end,max_points=50000))
                )


        data["datasets"] = datasets
        all_series = []
        for series in Series.objects.all():
            if str(series.id) in series_ids:
                series.selected = True
            all_series.append(series)
        data['all_series'] = all_series
        data['show_graph'] = True
    if graph_type == 'box-plot':
        series_ids = request.GET.getlist('series')
        datasets = []
        for sid in series_ids:
            series = get_object_or_404(Series,id=sid)
            lseries = LimitedSeries(series=series,start=start,end=end)
            datasets.append(lseries)

        data["datasets"] = datasets
        data["lsg"] = LimitedSeriesGroup(series=datasets)
        all_series = []
        for series in Series.objects.all():
            if str(series.id) in series_ids:
                series.selected = True
            all_series.append(series)
        data['all_series'] = all_series
        data['show_graph'] = False
        data['show_box_plot'] = len(datasets) > 0


    if graph_type == 'scatter-plot':
        independent = request.GET.get('independent',None)
        dependent = request.GET.get('dependent',None)

        if independent and dependent:
            ind_series = get_object_or_404(Series,id=independent)
            dep_series = get_object_or_404(Series,id=dependent)

            data["datasets"] = [dict(series=ind_series,
                                     lseries=LimitedSeries(series=ind_series,start=start,end=end)),
                                dict(series=dep_series,
                                     lseries=LimitedSeries(series=dep_series,start=start,end=end))
                                ]
            ind_data = ind_series.range_data(start,end,max_points=50000)
            dep_data = dep_series.range_data(start,end,max_points=50000)
            data['lseriesp'] = LimitedSeriesPair(independent=ind_series,
                                                 dependent=dep_series,
                                                 start=start,
                                                 end=end)
            data["data"] = zip(ind_data,dep_data)
            data["independent"] = ind_series
            data["dependent"] = dep_series

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
    data['graph_title'] = request.GET.get('title',"")
    return data


@rendered_with('waterquality/browse.html')
def browse(request):
    return dict(series=Series.objects.all())

@rendered_with('waterquality/series.html')
def series(request,id):
    series = get_object_or_404(Series,id=id)
    start = request.GET.get('start',False)
    if not start:
        start = series.start().timestamp
    end = request.GET.get('end',False)
    if not end:
        end = series.end().timestamp

    lseries = LimitedSeries(series=series,start=start,end=end)

    return dict(series=series,lseries=lseries)

@rendered_with('waterquality/series_all.html')
def series_all(request,id):
    series = get_object_or_404(Series,id=id)
    return dict(series=series)

def get_default_start():
    return Series.objects.all()[0].row_set.all()[0].timestamp

def get_default_end():
    return Series.objects.all()[0].row_set.all().order_by("-timestamp")[0].timestamp


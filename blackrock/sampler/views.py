from blackrock.sampler.models import Tree, Location
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import csv
import math


def import_csv(request):
    if request.method != 'POST':
        # TODO: this is a 500 error waiting to happen. views need to return
        # *something*
        return
    fh = request.FILES['csvfile']
    if file == '':
        # TODO: error checking (correct file type, etc.)
        url = request.build_absolute_uri("../admin/sampler/")
        return HttpResponseRedirect(url)

    # delete existing trees
    Location.objects.all().delete()
    Tree.objects.all().delete()

    table = csv.reader(fh)
    header = table.next()

    (id_idx, species_idx, x_idx, y_idx, dbh_idx,
     redirect_url) = header_indices(request, header)

    if redirect_url is not None:
        return HttpResponseRedirect(redirect_url)

    import_csv_table(table, id_idx, species_idx, x_idx, y_idx, dbh_idx)
    url = request.build_absolute_uri("../admin/sampler/tree")
    return HttpResponseRedirect(url)


def header_indices(request, header):
    for i in range(len(header)):
        h = header[i].lower()
        if h == 'id':
            id_idx = i
        elif h == 'species':
            species_idx = i
        elif h == 'x':
            x_idx = i
        elif h == 'y':
            y_idx = i
        elif h == 'dbh':
            dbh_idx = i
        else:
            url = request.build_absolute_uri("../admin/sampler/")
            return (None, None, None, None, url)
    return (id_idx, species_idx, x_idx, y_idx, dbh_idx, None)


def import_csv_table(table, id_idx, species_idx, x_idx, y_idx, dbh_idx):
    for row in table:
        id = row[id_idx]
        species = row[species_idx]
        x = row[x_idx]
        y = row[y_idx]
        dbh = row[dbh_idx]
        loc, created = Location.objects.get_or_create(x=x, y=y)
        Tree.objects.get_or_create(
            id=id, location=loc, species=species, dbh=dbh)


def index(request):
    return render_to_response('sampler/index.html')


def plot(request):
    # handle form data if present (will happen if doing "back" from later
    # forms)
    arglist = {}
    try:
        arglist = {'x_offset': request.POST['x-offset'],
                   'y_offset': request.POST['y-offset'],
                   'scale': request.POST['scale'],
                   'plot_h': request.POST['plot-h'],
                   'plot_w': request.POST['plot-w'],
                   }
    except:
        pass

    tree_list = Tree.objects.all()
    max_x = Location.objects.all().order_by('x').reverse()[0].x
    max_y = Location.objects.all().order_by('y').reverse()[0].y

    arglist.update({
                   'trees': tree_list,
                   'max_x': max_x,
                   'max_y': max_y,
                   })

    return render_to_response('sampler/plot.html', arglist)


def transect(request):
    try:
        x_offset = request.POST['x-offset']
        y_offset = request.POST['y-offset']
        scale = request.POST['scale']
        view_height = request.POST['view-height']
        view_width = request.POST['view-width']
        plot_h = request.POST['plot-h']
    except:
        # need to display error: "Please choose a plot area first."
        return HttpResponseRedirect("plot")

    # get transect data if provided (from later form)
    transect_start_x = ""
    transect_start_y = ""
    transect_end_x = ""
    transect_end_y = ""
    try:
        transect_start_x = request.POST['transect-start-x']
        transect_start_y = request.POST['transect-start-y']
        transect_end_x = request.POST['transect-end-x']
        transect_end_y = request.POST['transect-end-y']
    except:
        pass

    # find trees that are in the selected view
    visible_x_min = (0 - float(x_offset)) / float(scale) - 1
    visible_x_max = (float(view_width) - float(x_offset)) / float(scale) + 1

    visible_y_min = (float(plot_h) - float(
        view_height) + float(y_offset)) / float(scale) - 1
    visible_y_max = ((float(plot_h) + float(y_offset))) / float(scale) + 1

    valid_locations = Location.objects.filter(
        x__range=(str(visible_x_min), str(visible_x_max)),
        y__range=(str(visible_y_min), str(visible_y_max)))
    tree_list = Tree.objects.filter(location__in=valid_locations)

    # update tree locations
    xlocs = {}
    ylocs = {}
    for tree in tree_list:
        new_x = float(tree.location.x) + float(x_offset) / float(scale)
        new_y = (float(tree.location.y) -
                 (float(plot_h) - float(view_height) +
                  float(y_offset)) / float(scale))
        xlocs[tree.id] = new_x
        ylocs[tree.id] = new_y

    return render_to_response('sampler/transect.html', {
                              'trees': tree_list,
                              'scale': scale,
                              'x_offset': x_offset,
                              'y_offset': y_offset,
                              'xlocs': xlocs,
                              'ylocs': ylocs,
                              'plot_w': request.POST['plot-w'],
                              'plot_h': request.POST['plot-h'],
                              'view_height': view_height,
                              'view_width': view_width,
                              'transect_start_x': transect_start_x,
                              'transect_start_y': transect_start_y,
                              'transect_end_x': transect_end_x,
                              'transect_end_y': transect_end_y,
                              })


def calculate_theta(x1, x2, y1, y2):
    b = x2 - x1
    c = y2 - y1
    a = math.hypot(b, c)

    if b == 0:
        if y2 > y1:
            theta = 0
        else:
            theta = 180
    elif c == 0:
        if x2 > x1:
            theta = 270
        else:
            theta = 90
    else:
        theta = math.degrees(
            math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))

        theta = adjust_theta_by_quadrant(theta, x1, x2, y1, y2)

    theta = math.radians(theta)
    return theta


def worksheet(request):
    try:
        x_offset = request.POST['x-offset']
        y_offset = request.POST['y-offset']
        scale = request.POST['scale']
        view_height = request.POST['view-height']
        view_width = request.POST['view-width']
        plot_h = request.POST['plot-h']
    except:
        # need to display error: "Please choose a plot area first."
        return HttpResponseRedirect("plot")

    # find trees that are in the selected view
    visible_x_min = (0 - float(x_offset)) / float(scale)
    visible_x_max = (float(view_width) - float(x_offset)) / float(scale)

    visible_y_min = (float(plot_h) - float(
        view_height) + float(y_offset)) / float(scale)
    visible_y_max = ((float(plot_h) + float(y_offset))) / float(scale)

    Location.objects.filter(
        x__range=(str(visible_x_min), str(visible_x_max)),
        y__range=(str(visible_y_min), str(visible_y_max)))
    tree_list = Tree.objects.all()

    # rotate trees so transect is vertical
    x1 = float(request.POST['transect-start-x'])
    y1 = float(request.POST['transect-start-y'])
    x2 = float(request.POST['transect-end-x'])
    y2 = float(request.POST['transect-end-y'])

    theta = calculate_theta(x1, x2, y1, y2)

    xlocs = {}
    ylocs = {}
    for tree in tree_list:
        new_x = math.cos(theta) * (float(tree.location.x) - x1) + \
            math.sin(theta) * (float(tree.location.y) - y1) + x1
        new_y = -1 * math.sin(theta) * (float(tree.location.x) - x1) + \
            math.cos(theta) * (float(tree.location.y) - y1) + y1
        new_x = new_x + float(x_offset) / float(scale)
        new_y = (new_y -
                 (float(plot_h) - float(view_height) +
                  float(y_offset)) / float(scale))
        xlocs[tree.id] = new_x  # + 30
        ylocs[tree.id] = new_y  # + 16

    return render_to_response('sampler/worksheet.html', {
                              'trees': tree_list,
                              'xlocs': xlocs,
                              'ylocs': ylocs,
                              'range': range(1, 21),
                              'transect_start_x': x1,
                              'transect_start_y': y1,
                              'transect_end_x': x2,
                              'transect_end_y': y2,
                              'scale': scale,
                              'x_offset': x_offset,
                              'y_offset': y_offset,
                              'plot_w': request.POST['plot-w'],
                              'plot_h': request.POST['plot-h'],
                              'view_height': view_height,
                              'view_width': view_width,
                              })


def adjust_theta_by_quadrant(theta, x1, x2, y1, y2):
    # adjust theta depending on the quadrant
    # (always rotating clockwise, just to keep things simple)
    if x2 > x1 and y2 > y1:
        theta = 360 - 90 - theta
    elif x2 > x1 and y2 < y1:
        theta = 360 - (90 + theta)
    elif x2 < x1 and y2 < y1:
        theta = 180 - (theta - 90)
    else:
        theta = theta - 90
    return theta


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename=sampler-worksheet.csv'
    writer = csv.writer(response)

    # write headers
    headers = ['Quadrant Number', 'ID', 'Species', 'Distance', 'DBH']
    writer.writerow(headers)

    # write data
    for i in range(1, 21):
        row = []
        id = request.POST['%s-id' % i]
        if(id):
            tree = Tree.objects.get(id=id)
            distance = request.POST['%s-distance' % i]
            row = [i, id, tree.species, distance, tree.dbh]
            writer.writerow(row)

    return response


def csv_info(request):
    return render_to_response('sampler/csvinfo.html')

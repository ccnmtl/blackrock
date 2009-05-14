from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree, Plot
import csv, math

def index(request, admin_msg=""):

  #Plot.objects.all().delete()
  #Tree.objects.all().delete()
  #p = Plot(name="Mount Misery Plot", NE_corner='POINT(-74.025 41.39)', area=40000)
  #.save()

  #t = Tree(id=1, species="wo", dbh="5.5", location='POINT(-74.025 41.39)', plot=p)
  #t.save()
  #t2 = Tree(id=2, species="rm", dbh="3.5", location='POINT(-75.025 41.39)', plot=p)
  #t2.save()
  #p.update()

  return render_to_response('optimization/index.html',
                            context_instance=RequestContext(request))
                            
def run(request):
  return render_to_response('optimization/run.html')
  
def calculate(request):
  if request.method != 'POST':
    return HttpResponseRedirect("/respiration/")

  num_plots = float(request.REQUEST['numPlots'])
  shape = request.REQUEST['shape']
  diameter = float(request.REQUEST['diameter'])

  parent = Plot.objects.get(name="Mount Misery Plot")
  results = {}

  plot_results = {}
  total_time = 0
  for plot in range(num_plots):
    plot_results[plot] = calculate_plot(shape, diameter, parent)
    total_time += plot_results[plot]['time-total']

  results['plots'] = plot_results

  results['results-time'] = "%dh %dm" % (total_time / 60, total_time % 60)

  # TODO: sample variance density
  # TODO: sample variance basal area
  # TODO: sample area
  results['results-species'] = 10
  results['results-count'] = 321
  results['results-dbh'] = 23.4
  results['results-density'] = "TBD"
  results['results-basal'] = "TBD"
  # TODO: sample variance dbh
  
  # get actual results
  results['actual-area'] = round(parent.area * 100) / 100
  results['actual-species'] = int(parent.num_species)
  results['actual-count'] = int(parent.tree_set.count())
  results['actual-dbh'] = round(parent.mean_dbh * 100) / 100
  results['actual-density'] = round(float(parent.density) * 100) / 100
  results['actual-basal'] = round(float(parent.basal) * 100) / 100
  results['actual-variance-dbh'] = round(float(parent.variance_dbh) * 100) / 100
  
  return HttpResponse(str(results), mimetype="application/javascript")
  
  
def calculate_plot(shape, dimensions, parent):
  results = {}
  
  # TODO: determine plot
  
  ## number of trees in plot ##
  results['count'] = 100  #TODO
  
  ## area ##
  if shape == 'square':
    results['area'] = dimensions * dimensions
  else:
    results['area'] = math.pi * dimensions * dimensions
  
  ## time penalty ##

  # TODO: travel: 3 minutes per 100m (from NE corner? from previous plot?)
  results['time-travel'] = 5

  # locating a plot - 3 minutes per plot
  results['time-locate'] = 3

  # establishing plot boundaries (shape) - square = 5min, circle = 1.5min
  if shape == "square":
    results['time-establish'] = 5
  else:
    results['time-establish'] = 1.5

  # establishing plot boundaries (size) - larger plots take longer
  # (fudging at 1 minute per meter of diameter for now)
  results['time-establish'] += dimensions
  
  # measuring trees in the plot - 30 seconds per tree
  results['time-measure'] = .5 * results['count']
  
  results['time-total'] = results['time-travel'] + results['time-locate'] \
                        + results['time-establish'] + results['time-measure']
                        
                        
  return results

  
def loadcsv(request):
  if request.method == 'POST':
    
    fh = request.FILES['csvfile']
    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponseRedirect(request.build_absolute_uri("./"))

    # delete existing
    Plot.objects.all().delete()
    Tree.objects.all().delete()
    
    p = Plot(name="Mount Misery Plot", NE_corner='POINT(-74.025 41.39)', area=40000)
    p.save()

    table = csv.reader(fh)
    header = table.next()
    
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
        return HttpResponse("Unsupported header %s" % h)
      
    for row in table:
       id = row[id_idx]
       species = row[species_idx]
       x = float(row[x_idx])
       y = float(row[y_idx])
       dbh = row[dbh_idx]
       xloc = p.NE_corner.x - (0.001 * x)
       yloc = p.NE_corner.y - (0.001 * y)
       loc = 'POINT(%f %f)' % (xloc, yloc)  # TODO real location data
       tree = Tree.objects.get_or_create(id=id, location=loc, species=species, dbh=dbh, plot=p)

    p.precalc()
    return HttpResponseRedirect("optimization/")

def test(request):
  trees = Tree.objects.all()
  #for tree in trees:
    #print tree.location
  return render_to_response("optimization/test.html", {'trees':trees})
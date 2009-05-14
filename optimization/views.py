from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree, Plot
import csv

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

  results = {}  

  # calculate time penalty
  minutes = 0

  # TODO: travel: 3 minutes per 100m

  # locating a plot - 3 minutes per plot
  minutes = minutes + 3 * num_plots

  # establishing plot boundaries (shape) - square = 5min, circle = 1.5min
  if shape == "square":
    minutes = minutes + 5
  else:
    minutes = minutes + 1.5

  # establishing plot boundaries (size) - larger plots take longer
  # (fudging at 1 minute per meter of diameter for now)
  minutes = minutes + diameter
  
  # TODO: measuring trees in the plot - 30 seconds per tree
  #minutes = minutes + num_trees

  total_time = "%dh %dm" % (minutes / 60, minutes % 60)

  results['results-time'] = total_time
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
  plot = Plot.objects.get(name="Mount Misery Plot")
  plot.precalc()
  results['actual-area'] = round(plot.area * 100) / 100
  results['actual-species'] = int(plot.num_species)
  results['actual-count'] = int(plot.tree_set.count())
  results['actual-dbh'] = round(plot.mean_dbh * 100) / 100
  results['actual-density'] = round(float(plot.density) * 100) / 100
  results['actual-basal'] = round(float(plot.basal) * 100) / 100
  results['actual-variance-dbh'] = round(float(plot.variance_dbh) * 100) / 100
  
  return HttpResponse(str(results), mimetype="application/javascript")
  
  
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
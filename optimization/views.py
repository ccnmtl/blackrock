from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree, Plot
import csv, math, random, sets

NE_corner = 'POINT(-74.025 41.39)'
MULTIPLIER = 0.001   # to convert meters into degrees

def index(request, admin_msg=""):
  return render_to_response('optimization/index.html',
                            context_instance=RequestContext(request))
                            
def run(request):
  return render_to_response('optimization/run.html')
  
def calculate(request):
  if request.method != 'POST':
    return HttpResponseRedirect("/respiration/")

  num_plots = int(request.REQUEST['numPlots'])
  shape = request.REQUEST['shape']
  diameter = float(request.REQUEST['diameter'])

  parent = Plot.objects.get(name="Mount Misery Plot")
  parent.precalc()
  results = {}

  plot_results = {}
  total_time = 0
  results['sample-area'] = 0
  species_list = sets.Set()
  results['sample-count'] = 0
  intermed_dbh = 0
  results['sample-dbh'] = 0
  density_list = []
  results['sample-density'] = 0
  basal_list = []
  results['sample-basal'] = 0
  dbh_list = []

  for plot in range(num_plots):
    sub = sample_plot(shape, diameter, parent)

    total_time += sub['time-total']
    results['sample-area'] += sub['area']
    # TODO: sample variance density
    # TODO: sample variance basal area
    species_list = species_list.union(sub['species-list'])
    results['sample-count'] += sub['count']
    intermed_dbh += sub['dbh'] * sub['count']

    results['sample-density'] += sub['density']
    density_list.append(sub['density'])

    results['sample-basal'] += sub['basal']
    basal_list.append(sub['basal'])

    # sample variance dbh
    trees = sub['trees']
    for tree in trees:
      dbh_list.append(float(tree.dbh))
    sub['trees'] = ''

    sub['species-list'] = ""
    plot_results[plot] = sub

  results['plots'] = plot_results
  
  if total_time > 59:
    results['sample-time'] = "%dh %dm" % (total_time / 60, total_time % 60)
  else:
    results['sample-time'] = "%dm" % total_time
  results['sample-species'] = len(species_list)
  
  results['sample-area'] = round(results['sample-area'] * 100) / 100

  ## sample mean dbh ##
  if results['sample-count'] > 0:
    results['sample-dbh'] = round( (intermed_dbh / results['sample-count']) * 100) / 100
  else:
    results['sample-dbh'] = 0

  ## sample mean basal area ##
  results['sample-basal'] = round( (results['sample-basal'] / num_plots) * 100) / 100 # average

  ## sample mean density ##
  results['sample-density'] = round( (results['sample-density'] / num_plots) * 100) / 100 # average

  ## sample variance dbh ##
  if results['sample-count'] > 1:
    variance_sum = 0
    for dbh in dbh_list:
      variance_sum += (dbh - results['sample-dbh']) ** 2
    results['sample-variance-dbh'] = round( (math.sqrt( variance_sum / (results['sample-count']-1) ) ) * 100) / 100
  else:
    results['sample-variance-dbh'] = 0 

  if num_plots > 1:
    ## sample variance density ##
    density_sum = 0
    for density in density_list:
      density_sum += (density - results['sample-density']) **2
    results['sample-variance-density'] = round( math.sqrt( density_sum / (num_plots-1) ) * 100) / 100

    ## sample variance basal area ##
    basal_sum = 0
    for basal in basal_list:
      basal_sum += (basal - results['sample-basal']) **2
    results['sample-variance-basal'] = round( math.sqrt( basal_sum / (num_plots-1) ) * 100) / 100

  else:
    results['sample-variance-density'] = 0
    results['sample-variance-basal'] = 0
  
  # actual forest stats
  results['actual-area'] = round(parent.area * 100) / 100
  results['actual-species'] = int(parent.num_species)
  results['actual-count'] = int(parent.tree_set.count())
  results['actual-dbh'] = round(parent.mean_dbh * 100) / 100
  results['actual-density'] = round(float(parent.density) * 100) / 100
  results['actual-basal'] = round(float(parent.basal) * 100) / 100
  results['actual-variance-dbh'] = round(float(parent.variance_dbh) * 100) / 100
  
  return HttpResponse(str(results), mimetype="application/javascript")
  
  
def sample_plot(shape, dimensions, parent):
  results = {}
  
  ## determine plot ##
  # terrible, awful, ugly hack for now
  trees = None
  x = 0
  y = 0
  if shape == 'square':
    # pick a random NE corner
    # range = 0 - 200-dimensions
    x = random.randint(0, 200-dimensions)
    y = random.randint(0, 200-dimensions)
    dimensions_deg = MULTIPLIER * dimensions
    x_deg = MULTIPLIER * x
    y_deg = MULTIPLIER * y
    sample = 'POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))' \
              % (parent.NE_corner.x - x_deg, parent.NE_corner.y - y_deg, \
                 parent.NE_corner.x - x_deg - dimensions_deg, parent.NE_corner.y - y_deg, \
                 parent.NE_corner.x - x_deg - dimensions_deg, parent.NE_corner.y - y_deg - dimensions_deg, \
                 parent.NE_corner.x - x_deg, parent.NE_corner.y  - y_deg - dimensions_deg, \
                 parent.NE_corner.x - x_deg, parent.NE_corner.y - y_deg,                 
                 )
    trees = Tree.objects.filter(location__contained=sample)
  if shape == 'circle':
    # pick a random center point
    # range = dimensions - 200-dimensions
    x = random.randint(dimensions, 200-dimensions)
    y = random.randint(dimensions, 200-dimensions)
    x_deg = parent.NE_corner.x - x * MULTIPLIER
    y_deg = parent.NE_corner.y - y * MULTIPLIER
    center_pt = 'POINT (%s %s)' % (x_deg, y_deg)
    trees = Tree.objects.filter(location__dwithin=(center_pt, dimensions * MULTIPLIER))
 
  results['trees'] = trees
 
  ## number of trees in plot ##
  results['count'] = int(trees.count())

  species_list = sets.Set()
  dbh_sum = 0
  for tree in trees:
    species_list.add(tree.species)
    dbh_sum += tree.dbh

  results['species'] = len(species_list)
  results['species-list'] = species_list
  if trees.count() > 0:
    results['dbh'] = round(dbh_sum / trees.count() * 100) / 100
  else:
    results['dbh'] = 0
    
  ## dbh variance ##
  variance_sum = 0
  if results['count'] > 1:
    for tree in trees:
      variance_sum += (float(tree.dbh) - results['dbh']) ** 2
    results['variance-dbh'] = round( (math.sqrt( variance_sum / (results['count']-1) ) ) * 100) / 100
  else:
    results['variance-dbh'] = 0 

  ## area ##
  if shape == 'square':
    results['area'] = round(dimensions * dimensions * 100) / 100
  else:
    results['area'] = round(math.pi * dimensions * dimensions * 100) / 100
  
  ## basal area ##
  results['basal'] = round(( (float(dbh_sum) * 0.785398) / float(results['area']) ) * 100) / 100
   
  ## density ##
  results['density'] = round((trees.count() * 10000 / results['area']) * 100) / 100

  ## time penalty ##

  # travel: 3 minutes per 100m (TODO: from NE corner? from previous plot?)
  travel_distance = math.sqrt(x**2 + y**2)
  results['time-travel'] = round((travel_distance / 100) * 3)

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
    
    p = Plot(name="Mount Misery Plot", NE_corner=NE_corner, area=40000)
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
       xloc = p.NE_corner.x - (MULTIPLIER * x)
       yloc = p.NE_corner.y - (MULTIPLIER * y)
       loc = 'POINT(%f %f)' % (xloc, yloc)  # TODO real location data
       tree = Tree.objects.get_or_create(id=id, location=loc, species=species, dbh=dbh, plot=p)

    p.precalc()
    return HttpResponseRedirect("/optimization/")

def test(request):
  trees = Tree.objects.all()
  plot = Plot.objects.get(name="Mount Misery Plot")
  sample = sample_plot("square", 5, plot)['sample']
  return render_to_response("optimization/test.html", {'trees':trees, 'sample':sample})
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from blackrock.optimization.models import Tree, Plot
import csv, math, random, sets
import simplejson as json
from django.db.models import Q

NW_corner = 'POINT(-74.025 41.39)'
MULTIPLIER = 0.001   # to convert meters into degrees
DEFAULT_PLOT = 'Mount Misery Plot'

species_key = {#'ae':'Ulmus americana (american elm)',
               'ba':'basswood',
               'bb':'Betula lenta (black birch)',
               'be':'beech',
               'bg':'Nyssa sylvatica (black gum)',
               #'bm':'bm',
               'bo':'Quercus velutina (black oak)',
               'ch':'chestnut',
               'co':'Quercus prinus (chestnut oak)',
               'dw':'dogwood',
               'hh':'Carpinus caroliniana (hop hornbeam)',
               'mw':'moosewood',
               'o':'oak (species unknown)',
               'ph':'pignut hickory',
               'rm':'red maple',
               'ro':'Quercus rubra (red oak)',
               'sa':'sassafras',
               'sb':'shadbush',
               'sh':'Carya ovata (shagbark hickory)',
               'sm':'Acer saccharum (sugar maple)',
               'swo':'Quercus bicolor (swamp white oak)',
               'u':'non-oak (species unknown)',
               'vp':'Viburnum prunifolium (viburnum prunifolium)',
               'wa':'Fraxinus americana (white ash)',
               'wo':'Quercus alba (white oak)',
               'ws':'white spruce',
               }
               
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
  size = float(request.REQUEST['size'])
  arrangement = request.REQUEST['plotArrangement']

  parent = Plot.objects.get(name=DEFAULT_PLOT)
  results = {}

  plot_results = {}
  total_time = 0
  species_list = sets.Set()
  results['sample-area'] = 0
  results['sample-count'] = 0
  results['sample-dbh'] = 0
  results['sample-density'] = 0
  results['sample-basal'] = 0
  intermed_dbh = 0
  density_list = []
  basal_list = []
  dbh_list = []
  try:
    sample = RandomSample(shape,size,parent,num_plots,arrangement)
  except AssertionError:
    return HttpResponseBadRequest(json.dumps({"error":"Plot size and/or plot count is too big"}),
                                  mimetype="application/javascript")
  for plot,point in enumerate(sample):
    sub = sample_plot(sample,point,plot)

    total_time += sub['time-total']
    results['sample-area'] += sub['area']
    # TODO: sample variance density
    # TODO: sample variance basal area
    species_list = species_list.union(sub['species-list'])
    results['sample-count'] += sub['count']
    intermed_dbh += sub['dbh'] * sub['count']   # weighted sum, to be used for average

    results['sample-density'] += sub['density']
    density_list.append(sub['density'])

    results['sample-basal'] += sub['basal']
    basal_list.append(sub['basal'])

    # sample variance dbh
    trees = sub['trees']
    for tree in trees:
      dbh_list.append(float(tree.dbh))

    sub['trees'] = ''
    sub['species-list'] = ''

    plot_results[plot] = sub

  results['plots'] = plot_results
  
  results['sample-time'] = format_time(total_time)
  avg_time = total_time / num_plots
  results['avg-time'] = format_time(avg_time)

  results['sample-species'] = len(species_list)
  
  results['sample-area'] = round2(results['sample-area'])

  ## sample mean dbh ##
  if results['sample-count'] > 0:
    results['sample-dbh'] = round2( intermed_dbh / results['sample-count'] )
  else:
    results['sample-dbh'] = 0

  ## sample mean basal area ##
  results['sample-basal'] = round2( results['sample-basal'] / num_plots ) # average

  ## sample mean density ##
  results['sample-density'] = round2( results['sample-density'] / num_plots ) # average

  ## sample variance dbh ##
  results['sample-variance-dbh'] = round2( variance(dbh_list, results['sample-dbh'], results['sample-count']-1) )

  ## sample variance density ##
  results['sample-variance-density'] = round2( variance(density_list, results['sample-density'], num_plots-1) )

  ## sample variance basal area ##
  results['sample-variance-basal'] = round2( variance(basal_list, results['sample-basal'], num_plots-1) )

  results['sample'] = {
    "details":{},
    "bounds":{ #should probably go into the model
      "top":parent.NW_corner.y,
      "bottom":parent.NW_corner.y - float(parent.height)*MULTIPLIER,
      "left":parent.NW_corner.x,
      "right":parent.NW_corner.x + float(parent.width)*MULTIPLIER,
      "width":float(parent.width)*MULTIPLIER,
      "height":float(parent.height)*MULTIPLIER,
      },
    }

  # actual forest stats
  results['actual-area'] = round2(parent.area)
  results['actual-species'] = int(parent.num_species)
  results['actual-count'] = int(parent.tree_set.count())
  results['actual-dbh'] = round2(parent.mean_dbh)
  results['actual-density'] = round2( float(parent.density) )
  results['actual-basal'] = round2( float(parent.basal) )
  results['actual-variance-dbh'] = round2( float(parent.variance_dbh) )
  
  # comparison percentages
  results['comparison-area'] = comparison(results['sample-area'], results['actual-area'])
  results['comparison-species'] = comparison(results['sample-species'], results['actual-species'])
  results['comparison-count'] = comparison(results['sample-count'], results['actual-count'])
  results['comparison-dbh'] = comparison(results['sample-dbh'], results['actual-dbh'])
  results['comparison-variance-dbh'] = comparison(results['sample-variance-dbh'], results['actual-variance-dbh'])
  results['comparison-density'] = comparison(results['sample-density'], results['actual-density'])
  results['comparison-basal'] = comparison(results['sample-basal'], results['actual-basal'])
  
  return HttpResponse(json.dumps(results), mimetype="application/javascript")
  #return HttpResponse(str(results), mimetype="application/javascript")
  
  
class RandomSample:
  """creates a set of random sampling points (based on init arguments)
  those points are then fed to sample_plot()
  In the future, this will be where different Plot Arrangements
     can be calculated, but for now, we simply assure that points do not overlap,
     etc.
  """
  def __init__(self,shape,size,parent,num_plots,arrangement):
    self.errors = False

    self.shape = shape
    self.size = size
    self.parent = parent
    self.arrangement = arrangement

    delta = 0
    if self.shape == 'circle':
      delta = size

    if arrangement=='random':
      self.points = [{'x':random.randint(0, float(parent.width) - size),
                      'y':random.randint(0, float(parent.height) - size),
                      } for p in xrange(num_plots)]

    elif arrangement=='grid':
      w = float(parent.width) 
      w -= (w % size) 
      h = float(parent.height) 
      h -= (h % size) 
      #this is sloppy-- a fractional size might not fit within

      plots_avail = w*h / ((size+delta)**2)

      assert plots_avail > num_plots

      #floor cuts the remainder--maybe we should be using it somehow
      plots_across = math.floor( w/(size+delta) )

      self.choices = random.sample(xrange(int(plots_avail)), num_plots)
      self.points = [{'x':(p % plots_across  * (size+delta))+delta,
                      'y':(math.floor(p / plots_across)  * (size+delta))+delta
                      } 
                     for p in self.choices]
    

  def __iter__(self):
    return iter(self.points)

  def time_establish(self, point):
    # establishing plot boundaries (shape)
    t = {'square':5,
         'circle':1.5,
         }
    # establishing plot boundaries (size) - larger plots take longer
    # (fudging at 1 minute per meter of diameter for now)
    return t[self.shape] + self.size

  def area(self, point):
    a = {'square':lambda s:round2(s **2 ),
         'circle':lambda s:round2(math.pi * s * s),
         }
    return a[self.shape](self.size)

  def Q(self, point):
    go = {'square':self.squareQ,
          'circle':self.circleQ,
          }
    return go[self.shape](point)

  def polygon(self,point):
    go = {'square':self.squarePoints,
          'circle':self.circlePoints,
          }
    return go[self.shape](point)

  def squarePoints(self, point):
    par = self.parent
    size_deg = MULTIPLIER * self.size
    x_deg = MULTIPLIER * point['x'] + par.NW_corner.x 
    y_deg = par.NW_corner.y - MULTIPLIER * point['y']
    return ( (x_deg,            y_deg),
             (x_deg + size_deg, y_deg), 
             (x_deg + size_deg, y_deg - size_deg), 
             (x_deg,            y_deg - size_deg),
             )

  def circlePoints(self, point):
    "Lazily gives a hexagon"
    x_deg = self.parent.NW_corner.x + point['x'] * MULTIPLIER
    y_deg = self.parent.NW_corner.y - point['y'] * MULTIPLIER
    rad = self.size * MULTIPLIER
    point_num = 20

    return [(x_deg + rad*math.cos(angle) , y_deg + rad*math.sin(angle)) 
            for angle in 
            [math.pi*2*n/point_num for n in range(point_num)]
            ]

  def squareQ(self, point):
    points = [' '.join( (str(p[0]),str(p[1])) ) for p in self.squarePoints(point)]
    sample = ('POLYGON ((%s, %s, %s, %s, %s))' %
              (points[0], points[1], points[2], points[3], points[0])
              )

    return Q(location__contained=sample)
    
  def circleQ(self,point):
    x_deg = self.parent.NW_corner.x + point['x'] * MULTIPLIER
    y_deg = self.parent.NW_corner.y - point['y'] * MULTIPLIER
    center_pt = 'POINT (%s %s)' % (x_deg, y_deg)
    return Q(location__dwithin=(center_pt, self.size * MULTIPLIER))
    
  def travel_time(self,point):
    # travel: 3 minutes per 100m (TODO: from NE corner? from previous plot?)
    travel_distance = math.sqrt(point['x']**2 + point['y']**2)
    return round((travel_distance / 100) * 3)

def sample_plot(sample, point, p_index):
  "Calculates detailed statistics for a plot sample around a point"
  results = {}
  
  ## determine plot ##
  # terrible, awful, ugly hack for now
  trees = None

  trees = Tree.objects.filter( sample.Q(point) )

  results['coordinates'] = sample.polygon(point)

  results['trees'] = trees
 
  ## number of trees in plot ##
  results['count'] = int(trees.count())

  ## unique species ##
  species_list_intermed = sets.Set([str(tree.species).lower() for tree in trees])
  #if_else = lambda cond, a, b: [b,a][cond]
  #results['species-list'] = [if_else(species_key.has_key(species),species_key[species],species) for species in species_list_intermed]
  species_list = [species_key[species] for species in species_list_intermed if species_key.has_key(species)]
  species_list.extend([species for species in species_list_intermed if not species_key.has_key(species)])  # not in key
  results['species-list'] = species_list
                            
  results['num-species'] = len(results['species-list'])

  ## mean dbh ##
  dbhs = [float(tree.dbh) for tree in trees]
  dbh_sum = sum(dbhs)
  if trees.count() > 0:
    results['dbh'] = round2( dbh_sum / trees.count() )
  else:
    results['dbh'] = 0

  ## dbh variance ##
  results['variance-dbh'] = round2( variance(dbhs, results['dbh'], results['count']-1) )
    
  ## area ##
  results['area'] = sample.area(point)

  ## basal area ##
  results['basal'] = round2( (float(dbh_sum) * 0.785398) / float(results['area']) )

  ## density ##
  results['density'] = round2( (trees.count() * 10000) / results['area'] )

  ## time penalty ##

  results['time-travel'] = sample.travel_time(point)


  # locating a plot - 3 minutes per plot
  results['time-locate'] = 3

  # establishing plot boundaries (shape)
  results['time-establish'] = sample.time_establish(point)
  
  # measuring trees in the plot - 30 seconds per tree
  results['time-measure'] = .5 * results['count']
  
  results['time-total'] = results['time-travel'] + results['time-locate'] \
                        + results['time-establish'] + results['time-measure']
                        

  ## species results
  species_totals = {}
  i = 0
  for species in species_list_intermed:
    tree_count = len([tree.id for tree in trees if tree.species == species])
    
    # shortcut -- if there is only 1 species, use the plot results
    species_name = species
    if species_key.has_key(species): species_name = species_key[species]

    if(tree_count == results['count']):
      species_totals[i] = {'name': species_name, 'count': tree_count,
                           'dbh': results['dbh'],
                           'density': results['density'],
                           'basal': results['basal'],
                           'variance-dbh': results['variance-dbh']}

    else:
      dbhs = [float(tree.dbh) for tree in trees if tree.species == species]
      dbh_sum = sum(dbhs)
      mean_dbh = dbh_sum/tree_count
      species_totals[i] = {'name':species_name, 'count':tree_count,
                           'dbh': round2(mean_dbh),
                           'density': round2( (tree_count * 10000) / results['area'] ),
                           'basal': round2( (float(dbh_sum) * 0.785398) / float(results['area']) ),
                           'variance-dbh':round2( variance(dbhs, mean_dbh, tree_count-1) )
                           }
    i += 1
  results['species-totals'] = species_totals

  return results

def export_csv(request):
  results = request.POST['results']
  if(results == ''): return HttpResponse("")

  type = request.POST['type']
  
  results = json.loads(results)

  response = HttpResponse(mimetype='text/csv')
  response['Content-Disposition'] = 'attachment; filename=results.csv'
  writer = csv.writer(response)

  # write summary results
  writer.writerow(['**SAMPLING SUMMARY AND ANALYSIS**'])
  writer.writerow(['TIME TO SAMPLE', 'AVERAGE TIME PER PLOT', 'SAMPLE VARIANCE DENSITY', 'SAMPLE VARIANCE BASAL AREA'])
  writer.writerow([results['sample-time'], results['avg-time'], results['sample-variance-density'], results['sample-variance-basal']])

  writer.writerow([])
  
  writer.writerow(['', 'AREA', 'SPECIES', '# OF TREES', 'MEAN DBH', 'VARIANCE DBH', 'DENSITY', 'BASAL AREA'])
  writer.writerow(['SAMPLE PLOTS', results['sample-area'], results['sample-species'], results['sample-count'],
                   results['sample-dbh'], results['sample-variance-dbh'], results['sample-density'], results['sample-basal']])
  writer.writerow(['FOREST POPULATION', results['actual-area'], results['actual-species'], results['actual-count'],
                   results['actual-dbh'], results['actual-variance-dbh'], results['actual-density'], results['actual-basal']])
  writer.writerow(['COMPARISON', results['comparison-area'], results['comparison-species'], results['comparison-count'],
                   results['comparison-dbh'], results['comparison-variance-dbh'], results['comparison-density'], results['comparison-basal']])
                   
  writer.writerow([])
  writer.writerow([])

  # write plot summaries
  writer.writerow(['**PLOT SUMMARIES**'])

  writer.writerow(['PLOT NUMBER', 'PLOT AREA', 'TREES', 'TOTAL SAMPLING TIME'])
  plots = results['plots']
  for plot in sorted(plots.keys()):
    plotinfo = results['plots'][plot]
    row = [int(plot)+1, plotinfo['area'], plotinfo['count'], plotinfo['time-total']]
    #id = request.POST['%s-id' % i]
    #if(id):
    #  tree = Tree.objects.get(id=id)
    #  distance = request.POST['%s-distance' % i]
    #  row = [i, id, tree.species, distance, tree.dbh]
    writer.writerow(row)

  if type == "details":
    writer.writerow([])
    writer.writerow([])
    writer.writerow(["**PLOT DETAILS**"])
    writer.writerow(['PLOT NUMBER', 'SPECIES', '# OF TREES', 'MEAN DBH', 'VARIANCE DBH', 'DENSITY', 'BASAL AREA'])
    for plot in sorted(plots.keys()):
      plotinfo = results['plots'][plot]
      speciestotals = plotinfo['species-totals']
      #print sorted(speciestotals.keys())
      for species in sorted(speciestotals.keys()):
        speciesinfo = speciestotals[species]
        row = [int(plot)+1, speciesinfo['name'], speciesinfo['count'], speciesinfo['dbh'], speciesinfo['variance-dbh'],
                            speciesinfo['density'], speciesinfo['basal']]
        writer.writerow(row)
      writer.writerow([int(plot)+1, "TOTAL: %d" % len(speciestotals), plotinfo['count'], plotinfo['dbh'], plotinfo['variance-dbh'],
                                    plotinfo['density'], plotinfo['basal']])
      writer.writerow([])
  
  return response


## helper functions ##
def round2(value):
  # shortcut to round to 2 decimal places
  return round(value * 100) / 100
  
def comparison(thing1, thing2):
  # returns (sample / population) * 100
  comp = round2( (float(thing1) / float(thing2)) * 100 )
  return "%.2f%%" % comp

def format_time(time):
  # formats number of minutes in human-readable format
  if time > 59:
    hour = time / 60
    minute = time % 60
    if minute == 0:
      return "%d hr" % hour
    return "%d hr, %g min" % (hour, minute)
  else:
    return "%g min" % time

def variance(values, mean, population_size):
  # calculates variance
  if population_size < 1:
    return 0

  variance_sum = 0
  for value in values:
    variance_sum += (float(value) - mean)**2
  return variance_sum / population_size
  
def loadcsv(request):
  if request.method == 'POST':
    
    fh = request.FILES['csvfile']
    if file == '':
      # TODO: error checking (correct file type, etc.)
      return HttpResponse('No csv file specified')

    # delete existing
    Plot.objects.all().delete()
    Tree.objects.all().delete()
    
    p = Plot(name="Mount Misery Plot", NW_corner=NW_corner, area=67500, width=300, height=225)
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
      
    for row in table:
       id = row[id_idx]
       species = row[species_idx].lower()
       x = float(row[x_idx])
       y = float(row[y_idx])
       dbh = row[dbh_idx]
       xloc = p.NW_corner.x + (MULTIPLIER * x)
       yloc = p.NW_corner.y - (MULTIPLIER * y)
       loc = 'POINT(%f %f)' % (xloc, yloc)  # TODO real location data
       tree = Tree.objects.get_or_create(id=id, location=loc, species=species, dbh=dbh, plot=p)

    p.precalc()
    return HttpResponseRedirect("/optimization/")

def tree_png(request):
    parent = Plot.objects.get(name=DEFAULT_PLOT)
    image_margin = 10 #solves problem of error range in the MULTIPLIER
    x_delta = float(parent.width) *MULTIPLIER
    y_delta = float(parent.height) *MULTIPLIER
    x_deg = 0
    y_deg = 0
    c = parent.NW_corner
    sample = 'POLYGON ((%s %s, %s %s, %s %s, %s %s, %s %s))' \
             % (c.x + x_deg, c.y - y_deg, 
                c.x + x_deg + x_delta, c.y - y_deg, 
                c.x + x_deg + x_delta, c.y - y_deg - y_delta, 
                c.x + x_deg, c.y - y_deg - y_delta, 
                c.x + x_deg, c.y - y_deg,                 
                )
    trees = Tree.objects.filter(location__contained=sample)

    from PIL import Image
    dim = (parent.width+image_margin, parent.height+image_margin)
    im = Image.new("RGB", dim, "#CCFF77")
    for t in trees:
      im.putpixel(( int((t.location.x-c.x)/MULTIPLIER), int((c.y-t.location.y)/MULTIPLIER)), (00,256,00))
    response = HttpResponse(mimetype="image/png")
    im.crop( [0,0,int(parent.width),int(parent.height)] ).save(response, "PNG")
    #response['Cache-Control'] = 'max-age=%d'% 60*60*24*7
    return response


def test(request):
  trees = Tree.objects.all()
  plot = Plot.objects.get(name="Mount Misery Plot")
  #sample = sample_plot("square", 5, plot)['sample']
  return render_to_response("optimization/test.html", {'trees':trees})#, 'sample':sample})

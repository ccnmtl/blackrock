from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from mammals.models import *
from django.db.models import get_model, get_app
from django.utils.text import capfirst
from types import *    

class MammalSearchForm(SearchForm):
  habitat_list = [ (h.id, h.label ) for h in Habitat.objects.all()]
  species_list = [(s.id, s.common_name) for s in Species.objects.all()]
  
  csm = forms.CheckboxSelectMultiple
  trap_species = forms.MultipleChoiceField(required=False, label='Species', widget=csm, choices=species_list)
  trap_habitat = forms.MultipleChoiceField(required=False, label='Habitat', widget=csm, choices=habitat_list)
  
  def __init__(self, *args, **kwargs):
    super(MammalSearchForm, self).__init__(*args, **kwargs)
  
  
  if 1 == 0:
      def get_multiplechoicefield(self, name):
        print name
        query = ""
        if hasattr(self, "cleaned_data"):
          if name in self.cleaned_data:
            for a in self.cleaned_data[name]:
              if len(query):
                query += ' OR '
              query += "%s:%s" % (name, a)
        return query
  
  
  def checkboxes_or (self, name):
    """" note: this returns a blank string if nothing is checked."""
    return ' OR '.join (['%s:%s'% (name, a)  for a in self.cleaned_data[name]])


  #http://localhost:54321/mammals/species_map/51/
  
  def search(self):
    #import pdb
    #pdb.set_trace()
    
    
    
    sqs = []
    self.hidden = []
    if self.is_valid():
        #q = self.cleaned_data['q'].lower()
        #sqs = self.searchqueryset.auto_query(q)
        sqs = self.searchqueryset.auto_query('')
        #print "everything"
        #print len(sqs)
        #print sqs
        #print "trap locations"
        sqs = sqs.narrow('asset_type_exact:TrapLocation')
        #print len(sqs)
        #print sqs
        #print "narrowed by habitat"
        sqs = sqs.narrow (self.checkboxes_or ('trap_habitat'))      
        #print len(sqs)
        #print sqs
        #print "narrowed by species"
        sqs = sqs.narrow (self.checkboxes_or ('trap_species'))
        #print len(sqs)
        #print sqs
        if self.load_all:
            sqs = sqs.load_all()
    return sqs
    
class MammalSearchView(SearchView):
  #import pdb
  #pdb.set_trace()
  def __name__(self):
      return "MammalSearchView"
    
  def get_results(self):
    #import pdb
    #pdb.set_trace()
    print self.form.fields['trap_species'].choices[0]

    return self.form.search()
    
  def extra_context(self):
    extra = super(MammalSearchView, self).extra_context()
    if hasattr(self, "results"):
        if type(self.results) is ListType and len(self.results) < 1:
            extra["count"] = -1
        else:
            extra["count"] = len(self.results)
    query = ''
    for param, value in self.request.GET.items():
      if param != 'page':
        query += '%s=%s&' % (param, value) 
    extra['query'] = query
    extra['species'] = Species.objects.all()
    extra['habitats'] = Habitat.objects.all()
    return extra


    



    
    

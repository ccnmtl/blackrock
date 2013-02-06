from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from portal.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model, get_app
from django.utils.text import capfirst

#[06/Feb/2013 15:20:36] "GET /portal/search/?q=&asset_type=ForestStory&species=Animals&discipline=Forest+Ecology HTTP/1.1" 200 10885


class PortalSearchForm(SearchForm):

  def default_type_choices(site=None):
    if site is None:
        site = haystack.site
    
    choices = [(m._meta.object_name, m._meta.verbose_name) for m in site.get_indexed_models()]
    choices.sort()
    return choices
  
  def default_facet_choices(facet):
    
    choices = [ (f.name, f.display_name) for f in Facet.objects.filter(facet=facet)]
    choices.sort()
    return choices

  asset_type = forms.MultipleChoiceField(required=False, label=_('Record Type'), widget=forms.CheckboxSelectMultiple, choices=default_type_choices())
  study_type = forms.MultipleChoiceField(required=False, label=_('Study Type'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Study Type"))
  species = forms.MultipleChoiceField(required=False, label=_('Species'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Species"))
  discipline = forms.MultipleChoiceField(required=False, label=_('Discipline'), widget=forms.CheckboxSelectMultiple, choices=default_facet_choices("Discipline"))
  
  def __init__(self, *args, **kwargs):
    super(PortalSearchForm, self).__init__(*args, **kwargs)
  
  def get_multiplechoicefield(self, name):
    query = ""
    
    if hasattr(self, "cleaned_data"):
      if name in self.cleaned_data:
        for a in self.cleaned_data[name]:
          if len(query):
            query += ' OR '
          query += "%s:%s" % (name, a)
    print "called getmultiplechoice and returned ", query
    return query
  
  def search(self):
  
    
    #import pdb    
    #pdb.set_trace()
  
    sqs = []
    self.hidden = []

    if self.is_valid():
      q = self.cleaned_data['q'].lower()
      print "q is  ", q
      sqs = self.searchqueryset.auto_query(q)
      ordered_query = sqs.order_by("name")

      
      if self.load_all:
        sqs = sqs.load_all()
      
      for facet in Facet.asset_facets:
        sqs = sqs.facet(facet)
        if facet in self.fields:
          self.fields[facet].choices = []
        
      for facet in Facet.asset_facets:
        query = self.get_multiplechoicefield(facet)
        print "original query is ", query
        if len(query):
          print "narrowing with ", query
          sqs = sqs.narrow(query)

    # facet counts based on result set
    if len(sqs) > 0: ### this is broken
      counts = sqs.facet_counts()
      for facet in counts['fields']:
        if facet in self.fields:
          for key, value in counts['fields'][facet]:
            if value > 0:
              # Look up the display name for this facet
              display_name = key
              try:
                x = Facet.objects.get(name=key)
                display_name = x.display_name
              except:
                model = get_model("portal", key)
                if model:
                  display_name = capfirst(model._meta.verbose_name)
                
              choice = (key, "%s (%s)" % (display_name, value))
              self.fields[facet].choices.append(choice)
  
          self.fields[facet].choices.sort()
          
    return sqs
    
from types import *    
class PortalSearchView(SearchView):
  def __name__(self):
      return "PortalSearchView"
    
  def get_results(self):
    return self.form.search()
    
  def extra_context(self):
    extra = super(PortalSearchView, self).extra_context()
    if hasattr(self, "results"):
        if type(self.results) is ListType and len(self.results) < 1:
            extra["count"] = -1
        else:
            print "count is ",  len(self.results)
            extra["count"] = len(self.results)
      
    # @todo -- add latitude/longitude into the context. self.request.
    
    # Send down our current parameters minus page number
    query = ''
    for param, value in self.request.GET.items():
      if param != 'page':
        query += '%s=%s&' % (param, value) 
        print "extra query is " + query
    extra['query'] = query
    return extra

   
"""q is   a
called getmultiplechoice and returned  study_type:Long-Term OR study_type:Modeling
original query is  study_type:Long-Term OR study_type:Modeling
narrowing with  study_type:Long-Term OR study_type:Modeling
called getmultiplechoice and returned  
original query is  
called getmultiplechoice and returned  
original query is  
called getmultiplechoice and returned  asset_type:ResearchProject
original query is  asset_type:ResearchProject
narrowing with  asset_type:ResearchProject
called getmultiplechoice and returned  
original query is  
count is  6
extra query is q=a&
extra query is q=a&study_type=Modeling&
extra query is q=a&study_type=Modeling&asset_type=ResearchProject&
[06/Feb/2013 15:25:00] "GET /portal/search/?q=a&asset_type=ResearchProject&study_type=Long-Term&study_type=Modeling HTTP/1.1" 200 22435"""

    
    

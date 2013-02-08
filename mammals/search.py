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
    # note: the order in which these are defined... affects the order in which they are displayed in the template. This sucks but it's what I get for acquiescing to Django forms.
    trap_habitat = forms.MultipleChoiceField(required=False, label='Habitat', widget=csm, choices=habitat_list)
    trap_species = forms.MultipleChoiceField(required=False, label='Species', widget=csm, choices=species_list)

    def __init__(self, *args, **kwargs):
        super(MammalSearchForm, self).__init__(*args, **kwargs)

    def checkboxes_or (self, name):
        """" note: this returns a blank string if nothing is checked."""
        return ' OR '.join (['%s:%s'% (name, a)  for a in self.cleaned_data[name]])
        
    def search(self):
        sqs = []
        self.hidden = []
        if self.is_valid():
            sqs = self.searchqueryset.auto_query('')
            sqs = sqs.narrow('asset_type_exact:TrapLocation')
            sqs = sqs.narrow (self.checkboxes_or ('trap_habitat'))
            sqs = sqs.narrow (self.checkboxes_or ('trap_species'))
            if self.load_all:
                sqs = sqs.load_all()
        return sqs
    
class MammalSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        hella_many = 5000000000
        super(MammalSearchView, self).__init__(*args, **kwargs)
        self.results_per_page = hella_many
  
    def __name__(self):
        return "MammalSearchView"

    def get_results(self):
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
        
        #import pdb
        #pdb.set_trace()
        #search_map_repr
        extra ['results_json']= simplejson.dumps([tl.object.search_map_repr() for tl in self.results])

        return extra
        
        

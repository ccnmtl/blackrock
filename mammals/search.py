from django import forms
from haystack.views import SearchView, FacetedSearchView
from haystack.forms import *
from mammals.models import *
from django.db.models import get_model, get_app
from django.utils.text import capfirst
from types import *    
from collections import Counter
from django.utils import simplejson

class MammalSearchForm(SearchForm):

    success_list = [
        ('unsuccessful',          'Unsuccessful traps')
        ,('trapped_and_released', 'Trapped and released')
    ]
    
    signs_list = [
        ('observed',                'Observed')
        ,('camera',                 'Camera')
        ,('tracks_and_signs',       'Tracks and signs')
    ]
    
    habitat_list = [(h.id, h.label ) for h in Habitat.objects.all()]
    species_list = [(s.id, s.common_name) for s in Species.objects.all()]
    school_list =  [(s.id, s.name) for s in School.objects.all()]

    csm = forms.CheckboxSelectMultiple
    # note: the order in which these are defined... affects the order in which they are displayed in the template. This sucks but it's what I get for accepting to use Django forms.
    
    trap_success = forms.MultipleChoiceField(required=False, label='', widget=csm, choices=success_list)
    trap_signs =   forms.MultipleChoiceField(required=False, label='', widget=csm, choices=signs_list)
    
    trap_habitat = forms.MultipleChoiceField(required=False, label='Habitat', widget=csm, choices=habitat_list)
    trap_species = forms.MultipleChoiceField(required=False, label='Species', widget=csm, choices=species_list)
    trap_school = forms.MultipleChoiceField(required=False, label='School', widget=csm, choices=school_list)



    def __init__(self, *args, **kwargs):
        super(MammalSearchForm, self).__init__(*args, **kwargs)

    def checkboxes_or (self, name):
        """" note: this returns a blank string if nothing is checked."""
        return ' OR '.join (['%s:%s'% (name, a)  for a in self.cleaned_data[name]])
        
    def calculate_breakdown (self, the_sqs):
        result = {}
        for thing in  ['species', 'habitat', 'school', 'unsuccessful', 'trapped_and_released']:
            result [thing] = Counter ([getattr (x, ('trap_%s' % thing)) for x in the_sqs])
        
        # nanohack
        result['trap_success'] = {}
        result['trap_success']['unsuccessful']         = result['trapped_and_released'][False];
        result['trap_success']['trapped_and_released'] = result['trapped_and_released'][True ];


        #import pdb
        #pdb.set_trace()
        
            
        return simplejson.dumps(result)

    def search(self):
        sqs = []
        self.hidden = []
        if self.is_valid():
        
            
            #else
            
            ##TODO test validity of connection and throw error if there's a problem.
            sqs = self.searchqueryset.auto_query('')
            sqs = sqs.narrow ('asset_type_exact:TrapLocation')
            
            
            #not sure i want this...
            #if self.load_all:
            #    return sqs.load_all()
            
            sqs = sqs.narrow (self.checkboxes_or ('trap_habitat'))
            sqs = sqs.narrow (self.checkboxes_or ('trap_species'))
            sqs = sqs.narrow (self.checkboxes_or ('trap_school' ))
            
            #trap success:
            show_unsuccessful = 'unsuccessful'         in self.cleaned_data['trap_success']
            show_successful   = 'trapped_and_released' in self.cleaned_data['trap_success']
            # if neither, or both, are clicked, show all locations.
            # however:
            if show_unsuccessful and not show_successful:
                sqs = sqs.narrow('trap_unsuccessful:True')
            if show_successful   and not show_unsuccessful:
                sqs = sqs.narrow('trap_trapped_and_released:True')
            
            
            self.breakdown = self.calculate_breakdown(sqs)
            #import pdb
            #pdb.set_trace()    
        
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
        
        
        #self.form.breakdown ( the_sqs):

        #this is what's used to actually draw the form:
        if not hasattr(self.form, 'breakdown'):
            self.form.breakdown = {}
            
        extra ['results_json']= simplejson.dumps([tl.object.search_map_repr() for tl in self.results])

        return extra
        

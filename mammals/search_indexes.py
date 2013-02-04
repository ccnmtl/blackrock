import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import MultiValueField, CharField
from mammals.models import TrapLocation

class TrapLocationIndex(SearchIndex):

    text = CharField(document=True, use_template=True)
    
    trap_species = MultiValueField(faceted=True)
    trap_habitat = MultiValueField(faceted=True)

    def get_model(self):
        return TrapLocation
        
    def prepare_trap_name(self, obj):
        return obj.__unicode__()  

    def prepare_trap_species(self, obj):
        if obj.animal:
            return obj.animal.species.common_name
        else:
            return None
        
    def prepare_trap_habitat(self, obj):
        if obj.habitat:
            return obj.habitat.label
        else:
            return None

  
    #def prepare_categories(self, obj):
    #    # Since we're using a M2M relationship with a complex lookup,
    #    # we can prepare the list here.
    #    return [category.id for category in obj.category_set.active().order_by('-created')]
  
site.register(TrapLocation, TrapLocationIndex)

import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import MultiValueField, CharField
from mammals.models import TrapLocation

class TrapLocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #not used.
    
    trap_species = CharField(faceted=True)
    trap_habitat = CharField(faceted=True)
    asset_type = CharField(faceted=True)

    def get_model(self):
        return TrapLocation
        
    def prepare_trap_name(self, obj):
        return obj.__unicode__()  

    def prepare_trap_species(self, obj):
        if obj.animal:
            return obj.animal.species.id
        else:
            return None
        
    def prepare_trap_habitat(self, obj):
        if obj.habitat:
            return obj.habitat.id
        else:
            return None
            
    def prepare_asset_type(self, obj):
        return obj._meta.object_name
  
site.register(TrapLocation, TrapLocationIndex)





import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import CharField, BooleanField, DateTimeField
from mammals.models import TrapLocation

class TrapLocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #not used, but apparently mandatory.
    
    trap_species =              CharField     (faceted=True)
    trap_habitat =              CharField     (faceted=True)    
    trap_school  =              CharField     (faceted=True)
    
    trap_date    =              DateTimeField (faceted=True)
    
    trap_trapped_and_released = BooleanField     (faceted=True)
    trap_observed =             BooleanField     (faceted=True)
    trap_camera =               BooleanField     (faceted=True)
    trap_tracks_and_signs =     BooleanField     (faceted=True)
    trap_unsuccessful    =      BooleanField     (faceted=True)
    
    asset_type =                CharField     (faceted=True)

    def get_model(self):
        return TrapLocation
        
    def prepare_trap_name(self, obj):
        return obj.__unicode__()  

        
    def prepare_trap_species(self, obj):
        if obj.animal:
            print obj.animal
            return obj.animal.species.id
        else:
            return None
        
    def prepare_trap_habitat(self, obj):
        if obj.habitat:
            print obj.habitat
            return obj.habitat.id
        else:
            return None

    def prepare_trap_school(self, obj):
        return obj.school_if_any()
    
    def prepare_trap_date(self, obj):
        print obj.date_for_solr()
        return obj.date_for_solr()
        
    def prepare_trap_trapped_and_released(self, obj):
        if obj.animal:
            return True
        else:
            return False
            
    def prepare_trap_unsuccessful(self, obj):
        if obj.animal:
            return False
        else:
            return True 
            
    def prepare_trap_observed(self, obj):
        return False
        
    def prepare_trap_camera(self, obj):
        return False

    def prepare_trap_tracks_and_signs(self, obj):
        return False
            
    def prepare_asset_type(self, obj):
        return obj._meta.object_name


  
site.register(TrapLocation, TrapLocationIndex)



#    add indexing for 
#        epxeition date
#        school
#        trap_successful
#        trap_unsuccessful

#class BooleanField(SearchField):
#class DateTimeField(SearchField):


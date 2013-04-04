import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import CharField, BooleanField, DateTimeField
from mammals.models import TrapLocation, Sighting

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
    
    asset_type =                CharField        (faceted=True)

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

    def prepare_trap_school(self, obj):
        if obj.expedition.school:
            return obj.expedition.school.id
        else:
            return None
    
    def prepare_trap_date(self, obj):
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



class SightingIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #not used, but apparently mandatory.
    
    sighting_species =              CharField     (faceted=True)
    sighting_habitat =              CharField     (faceted=True)    
    sighting_school  =              CharField     (faceted=True)
    
    sighting_date    =              DateTimeField (faceted=True)
    
    sighting_trapped_and_released = BooleanField     (faceted=True)
    sighting_observed =             BooleanField     (faceted=True)
    sighting_camera =               BooleanField     (faceted=True)
    sighting_tracks_and_signs =     BooleanField     (faceted=True)
    sighting_unsuccessful    =      BooleanField     (faceted=True)
    
    asset_type =                CharField        (faceted=True)

    def get_model(self):
        return Sighting
        
    def prepare_sighting_name(self, obj):
        return obj.__unicode__()  
    
    def prepare_sighting_species(self, obj):
        if obj.species:
            return obj.species.id
        else:
            return None
        
    def prepare_sighting_habitat(self, obj):
        if obj.habitat:
            return obj.habitat.id
        else:
            return None

    def prepare_sighting_school(self, obj):
        return None
    
    def prepare_sighting_date(self, obj):
        return obj.date_for_solr()
        
    def prepare_sighting_trapped_and_released(self, obj):
        return False
            
    def prepare_sighting_unsuccessful(self, obj):
        return False 

    def prepare_sighting_observed(self, obj):
        if obj.observation_type and obj.observation_type.label in ['Sighting']:
            return True
        else:
            return False
        
    def prepare_sighting_camera(self, obj):
        if obj.observation_type and obj.observation_type.label in ['Camera-trapped']:
            return True
        else:
            return False

    def prepare_sighting_tracks_and_signs(self, obj):
        if obj.observation_type and obj.observation_type.label not in ['Sighting','Camera-trapped']:
            return True
        else:
            return False
            
    def prepare_asset_type(self, obj):
        return obj._meta.object_name
            
    def prepare_asset_type(self, obj):
        return obj._meta.object_name


  
site.register(Sighting, SightingIndex)



#    add indexing for 
#        epxeition date
#        school
#        trap_successful
#        trap_unsuccessful

#class BooleanField(SearchField):
#class DateTimeField(SearchField):


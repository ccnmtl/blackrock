import datetime
from haystack import site
from haystack.indexes import RealTimeSearchIndex, SearchIndex
from haystack.fields import CharField, BooleanField, DateTimeField
from mammals.models import TrapLocation, Sighting

class TrapLocationIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #not used, but apparently mandatory.
    
    
    species_id =           CharField        (faceted=True)
    
    habitat =              CharField        (faceted=True)    
    school  =              CharField        (faceted=True)
    
    
    species_label =        CharField        (faceted=True)
    habitat_label =        CharField        (faceted=True)    
    school_label  =        CharField        (faceted=True)
    
    lat =                  CharField        (faceted=True)
    lon =                  CharField        (faceted=True)
    date    =              DateTimeField    (faceted=True)
    trapped_and_released = BooleanField     (faceted=True)
    observed =             BooleanField     (faceted=True)
    camera =               BooleanField     (faceted=True)
    tracks_and_signs =     BooleanField     (faceted=True)
    unsuccessful    =      BooleanField     (faceted=True)
    
    
    
    
    asset_type =                CharField        (faceted=True)

    def get_model(self):
        return TrapLocation
            
                
    def prepare_species_id(self, obj):
        if obj.animal:
            return obj.animal.species.id
        else:
            return None
            
        
    def prepare_habitat(self, obj):
        if obj.habitat:
            return obj.habitat.id
        else:
            return None

    def prepare_school(self, obj):
        if obj.expedition.school:
            return obj.expedition.school.id
        else:
            return None
            
    def prepare_habitat_label(self, obj):
        if obj.habitat:
            return obj.habitat.label
        else:
            return None
            
    def prepare_species_label(self, obj):
        if obj.animal:
            return obj.animal.species.common_name
        else:
            return None
            
    def prepare_school_label(self, obj):
        if obj.expedition.school:
            return obj.expedition.school.name
        else:
            return None
    
    def prepare_date(self, obj):
        return obj.date_for_solr()
        
    def prepare_trapped_and_released(self, obj):
        if obj.animal:
            return True
        else:
            return False
            
    def prepare_unsuccessful(self, obj):
        if obj.animal:
            return False
        else:
            return True 
            
            
    #these are not sightings, so none of these three is applicable:    
    def prepare_observed(self, obj):
        return None
        
    def prepare_camera(self, obj):
        return None

    def prepare_tracks_and_signs(self, obj):
        return None
        
        
    def prepare_lat(self, obj):
        return obj.actual_lat()
        
    def prepare_lon(self, obj):
        return obj.actual_lon()


    def prepare_asset_type(self, obj):
        return obj._meta.object_name
        

site.register(TrapLocation, TrapLocationIndex)

class SightingIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #not used, but apparently mandatory.
    
    species_id =              CharField        (faceted=True)
    habitat =              CharField        (faceted=True)    
    school  =              CharField        (faceted=True)
    
    species_label =         CharField        (faceted=True)
    habitat_label =         CharField        (faceted=True)    
    school_label  =         CharField        (faceted=True)
    
    date    =              DateTimeField    (faceted=True)
    lat =                  CharField        (faceted=True)
    lon =                  CharField        (faceted=True)    
    trapped_and_released = BooleanField     (faceted=True)
    unsuccessful    =      BooleanField     (faceted=True)
    observed =             BooleanField     (faceted=True)
    camera =               BooleanField     (faceted=True)
    tracks_and_signs =     BooleanField     (faceted=True)
    
    
    
    
    asset_type =                CharField        (faceted=True)

    def get_model(self):
        return Sighting
        
    def prepare_name(self, obj):
        return obj.__unicode__()  
    
    def prepare_species_id(self, obj):
        if obj.species:
            return obj.species.id
        else:
            return None
        
    def prepare_habitat(self, obj):
        if obj.habitat:
            return obj.habitat.id
        else:
            return None
            

    def prepare_school(self, obj):
        return None
    
    def prepare_habitat_label(self, obj):
        if obj.habitat:
            return obj.habitat.label
        else:
            return None
            
    def prepare_species_label(self, obj):
        #print obj
        #print obj.id
        if obj.species:
            #print  obj.species.common_name
            return obj.species.common_name
        else:
            return None
            
    def prepare_school_label(self, obj):
        return None
    
    
    def prepare_date(self, obj):
        return obj.date_for_solr()
        
        
        
    #these are not traps, so neither of these is applicable:    
    def prepare_trapped_and_released(self, obj):
        return None
            
    def prepare_unsuccessful(self, obj):
        return None 



    def prepare_observed(self, obj):
        if obj.observation_type and obj.observation_type.label in ['Sighting']:
            return True
        else:
            return False
        
    def prepare_camera(self, obj):
        if obj.observation_type and obj.observation_type.label in ['Camera-trapped']:
            return True
        else:
            return False

    def prepare_tracks_and_signs(self, obj):
        if obj.observation_type and obj.observation_type.label not in ['Sighting','Camera-trapped']:
            return True
        else:
            return False

    def prepare_asset_type(self, obj):
        return obj._meta.object_name
            

    def prepare_lat(self, obj):
        return obj.lat()
        
    def prepare_lon(self, obj):
        return obj.lon()
  
site.register(Sighting, SightingIndex)




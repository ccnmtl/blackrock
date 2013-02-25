from django.conf.urls.defaults import *
import os.path
from django.contrib import databrowse
from mammals.search import MammalSearchView, MammalSearchForm

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
	
	#Research version:
	(r'^$',              'blackrock.mammals.views.index' ),
	(r'^grid/$',          'blackrock.mammals.views.grid' ),
	(r'^grid_square/$',   'blackrock.mammals.views.grid_block' ),

    #printer and csv versions of the grid square:
	(r'^grid_square_csv/$',       'blackrock.mammals.views.grid_square_csv' ),
	(r'^grid_square_print/$',     'blackrock.mammals.views.grid_square_print' ),

	#Sandbox version:
	(r'^sandbox/$',              'blackrock.mammals.views.sandbox_grid' ),
	(r'^sandbox/grid/$',          'blackrock.mammals.views.sandbox_grid' ),
	(r'^sandbox/grid_square/$',   'blackrock.mammals.views.sandbox_grid_block' ),
	
	
	(r'^help/$',               'blackrock.mammals.views.help' ),
	(r'^teaching/$', 'blackrock.mammals.views.teaching_resources' ),


	(r'^login/$',                 'blackrock.mammals.views.mammals_login' ),
	(r'^process_login/$',         'blackrock.mammals.views.process_login' ),
	(r'^logout/$', 'django.contrib.auth.views.logout',  {'next_page': '/mammals/'}),
	
	(r'^all_expeditions/$',  'blackrock.mammals.views.all_expeditions' ),
	
	
	
	(r'^new_expedition_ajax/$',   'blackrock.mammals.views.new_expedition_ajax' ),
	
	
	(r'^expedition/(?P<expedition_id>\d+)/$', 'blackrock.mammals.views.expedition'),
	(r'^edit_expedition/(?P<expedition_id>\d+)/$', 'blackrock.mammals.views.edit_expedition'),
	(r'^edit_expedition_ajax/$', 'blackrock.mammals.views.edit_expedition_ajax'),
	
	
	(r'^expedition/(?P<expedition_id>\d+)/animals/$', 'blackrock.mammals.views.expedition_animals'),
	
	
	(r'^save_expedition_animals/$', 'blackrock.mammals.views.save_expedition_animals'),
	
	#prob. not needed/
	#(r'^save_expedition_animals_ajax/$', 'blackrock.mammals.views.save_expedition_animals_ajax'),
	
	
	(r'^team_form/(?P<expedition_id>\d+)/(?P<team_letter>\w+)/$', 'blackrock.mammals.views.team_form'),
	
	
	(r'^save_team_form/$', 'blackrock.mammals.views.save_team_form'),
	(r'^save_team_form_ajax/$', 'blackrock.mammals.views.save_team_form_ajax'),
	
	#TODO remove -- these are obsolete.
	#(r'^map_index/$',              'blackrock.mammals.views.map_index' ),	
	#(r'^species_map/$',              'blackrock.mammals.views.species_map' ),
	#(r'^species_map/(?P<species_id>\d+)/$',              'blackrock.mammals.views.species_map' ),
	#(r'^habitat_map/$',              'blackrock.mammals.views.habitat_map' ),
	#(r'^habitat_map/(?P<habitat_id>\d+)/$',              'blackrock.mammals.views.habitat_map' ),
    
    url(r'^search/', MammalSearchView(template="mammals/search.html", form_class=MammalSearchForm), name='search'),
	
	#(r'^selenium/(?P<task>\w+)/$',               'family_info.views.selenium'),

)

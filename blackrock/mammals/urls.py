from django.conf.urls import url
import os.path
from blackrock.mammals.search import MammalSearchView, MammalSearchForm

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': media_root}),

    # Research version:
    url(r'^$', 'blackrock.mammals.views.index'),
    url(r'^grid/$', 'blackrock.mammals.views.grid'),
    url(r'^grid_square/$',
        'blackrock.mammals.views.grid_block'),

    # printer and csv versions of the grid square:
    url(r'^grid_square_csv/$',
        'blackrock.mammals.views.grid_square_csv'),
    url(r'^grid_square_print/$',
        'blackrock.mammals.views.grid_square_print'),

    # Sandbox version:
    url(r'^sandbox/$',
        'blackrock.mammals.views.sandbox_grid'),
    url(r'^sandbox/grid/$',
        'blackrock.mammals.views.sandbox_grid'),
    url(r'^sandbox/grid_square/$',
        'blackrock.mammals.views.sandbox_grid_block'),

    url(r'^help/$',
        'blackrock.mammals.views.help'),
    url(r'^teaching/$', 'blackrock.mammals.views.teaching_resources'),

    url(r'^login/$',
        'blackrock.mammals.views.mammals_login'),

    url(r'^process_login/$',
        'blackrock.mammals.views.process_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/mammals/'}),

    url(r'^all_expeditions/$',
        'blackrock.mammals.views.all_expeditions'),

    url(r'^new_expedition_ajax/$',
        'blackrock.mammals.views.new_expedition_ajax'),

    url(r'^expedition/(?P<expedition_id>\d+)/$',
        'blackrock.mammals.views.expedition'),
    url(r'^edit_expedition/(?P<expedition_id>\d+)/$',
        'blackrock.mammals.views.edit_expedition'),
    url(r'^edit_expedition_ajax/$',
        'blackrock.mammals.views.edit_expedition_ajax'),

    url(r'^sightings/$', 'blackrock.mammals.views.sightings'),
    url(r'^create_sighting/$',
        'blackrock.mammals.views.create_sighting'),
    url(r'^sighting/(?P<sighting_id>\d+)/$',
        'blackrock.mammals.views.sighting'),
    url(r'^edit_sighting/$',
        'blackrock.mammals.views.edit_sighting'),

    url(r'^expedition/(?P<expedition_id>\d+)/animals/$',
        'blackrock.mammals.views.expedition_animals'),

    url(r'^save_expedition_animals/$',
        'blackrock.mammals.views.save_expedition_animals'),

    url(r'^team_form/(?P<expedition_id>\d+)/(?P<team_letter>\w+)/$',
        'blackrock.mammals.views.team_form'),

    url(r'^save_team_form/$',
        'blackrock.mammals.views.save_team_form'),
    url(r'^save_team_form_ajax/$',
        'blackrock.mammals.views.save_team_form_ajax'),

    url(r'^search/',
        MammalSearchView(template="mammals/search.html",
                         form_class=MammalSearchForm), name='search'),

    url(r'^ajax_search/$',
        'blackrock.mammals.search.ajax_search'),
]

from django.conf.urls import url
import os.path
import django.views.static
from django.contrib.auth.views import LogoutView

from .search import MammalSearchView, MammalSearchForm, ajax_search
from .views import (
    index, grid, grid_block, grid_square_csv, grid_square_print,
    process_login, save_team_form, all_expeditions,
    team_form, mammals_login, sandbox_grid, teaching_resources,
    sightings, edit_sighting, create_sighting, new_expedition_ajax,
    sandbox_grid_block, sighting, expedition, edit_expedition,
    save_team_form_ajax, edit_expedition_ajax, save_expedition_animals,
    expedition_animals, help,
)

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),

    # Research version:
    url(r'^$', index),
    url(r'^grid/$', grid),
    url(r'^grid_square/$', grid_block),

    # printer and csv versions of the grid square:
    url(r'^grid_square_csv/$', grid_square_csv),
    url(r'^grid_square_print/$', grid_square_print),

    # Sandbox version:
    url(r'^sandbox/$', sandbox_grid),
    url(r'^sandbox/grid/$', sandbox_grid),
    url(r'^sandbox/grid_square/$', sandbox_grid_block),

    url(r'^help/$', help),
    url(r'^teaching/$', teaching_resources),

    url(r'^login/$', mammals_login),

    url(r'^process_login/$', process_login),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': '/mammals/'}),

    url(r'^all_expeditions/$', all_expeditions),
    url(r'^new_expedition_ajax/$', new_expedition_ajax),
    url(r'^expedition/(?P<expedition_id>\d+)/$', expedition),
    url(r'^edit_expedition/(?P<expedition_id>\d+)/$', edit_expedition),
    url(r'^edit_expedition_ajax/$', edit_expedition_ajax),

    url(r'^sightings/$', sightings),
    url(r'^create_sighting/$', create_sighting),
    url(r'^sighting/(?P<sighting_id>\d+)/$', sighting),
    url(r'^edit_sighting/$', edit_sighting),

    url(r'^expedition/(?P<expedition_id>\d+)/animals/$', expedition_animals),
    url(r'^save_expedition_animals/$', save_expedition_animals),
    url(r'^team_form/(?P<expedition_id>\d+)/(?P<team_letter>\w+)/$',
        team_form),
    url(r'^save_team_form/$', save_team_form),
    url(r'^save_team_form_ajax/$', save_team_form_ajax),

    url(r'^search/',
        MammalSearchView(template="mammals/search.html",
                         form_class=MammalSearchForm), name='search'),

    url(r'^ajax_search/$', ajax_search),
]

from django.urls import path, re_path
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
    re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': media_root}),

    # Research version:
    path('', index),
    path('grid/', grid),
    path('grid_square/', grid_block),

    # printer and csv versions of the grid square:
    path('grid_square_csv/', grid_square_csv),
    path('grid_square_print/', grid_square_print),

    # Sandbox version:
    path('sandbox/', sandbox_grid),
    path('sandbox/grid/', sandbox_grid),
    path('sandbox/grid_square/', sandbox_grid_block),

    path('help/', help),
    path('teaching/', teaching_resources),

    path('login/', mammals_login),

    path('process_login/', process_login),
    path('logout/', LogoutView.as_view(), {'next_page': '/mammals/'}),

    path('all_expeditions/', all_expeditions),
    path('new_expedition_ajax/', new_expedition_ajax),
    re_path(r'^expedition/(?P<expedition_id>\d+)/$', expedition),
    re_path(r'^edit_expedition/(?P<expedition_id>\d+)/$', edit_expedition),
    path('edit_expedition_ajax/', edit_expedition_ajax),

    path('sightings/', sightings),
    path('create_sighting/', create_sighting),
    re_path(r'^sighting/(?P<sighting_id>\d+)/$', sighting),
    path('edit_sighting/', edit_sighting),

    re_path(r'^expedition/(?P<expedition_id>\d+)/animals/$',
            expedition_animals),
    path('save_expedition_animals/', save_expedition_animals),
    re_path(r'^team_form/(?P<expedition_id>\d+)/(?P<team_letter>\w+)/$',
            team_form),
    path('save_team_form/', save_team_form),
    path('save_team_form_ajax/', save_team_form_ajax),

    path('search/',
         MammalSearchView(template="mammals/search.html",
                          form_class=MammalSearchForm), name='search'),

    path('ajax_search/', ajax_search),
]

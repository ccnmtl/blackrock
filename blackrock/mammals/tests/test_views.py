from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.contrib.auth.models import User
from blackrock.mammals.views import process_login, index, grid_block
from django.http import HttpResponse, HttpResponseRedirect


class BasicViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()


    def test_index(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('mammals/index.html')

    # (r'^help/$',     'blackrock.mammals.views.help'),
    def test_help(self):
        response = self.c.get('/mammals/help/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/index.html')
        self.assertEqual(type(response), HttpResponse)

    # (r'^teaching/$', 'blackrock.mammals.views.teaching_resources'),
    def test_teaching(self):
        response = self.c.get('/mammals/teaching/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/teaching_resources.html')
        self.assertEqual(type(response), HttpResponse)

    # (r'^login/$',     'blackrock.mammals.views.mammals_login'),
    def test_login(self):
        response = self.c.get('/mammals/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/login.html')

    # (r'^process_login/$',     'blackrock.mammals.views.process_login'),
    def test_process_login_get_fail(self):
        response = self.c.get('/mammals/process_login/')
        self.assertEqual(response.status_code, 302)
        redirect = "mammals/login/"
        self.assertRedirects(response, redirect)
        #self.assertTemplateUsed('mammals/teaching_resources.html')

    # (r'^process_login/$',     'blackrock.mammals.views.process_login'),
    def test_process_login_post_fail(self):
        response = self.c.post('/mammals/process_login/')
        self.assertEqual(response.status_code, 302)
        redirect = "mammals/login/"
        self.assertRedirects(response, redirect)


    def test_process_login_auth_fail(self):
        request = self.factory.post('/mammals/process_login/', {"username" : "username", "password" : "password"})
        response = process_login(request)
        self.assertEqual(response.status_code, 403)
        # #actually in method says it should redirect to login page
        # self.assertEqual(response.status_code, 302)
        # redirect = "mammals/login/"
        # self.assertRedirects(response, redirect)

    # (r'^grid_square/$', 'blackrock.mammals.views.grid_block'),
    def test_gridblock_get(self):
        '''should redirect request to index'''
        response = self.c.get('/mammals/grid_square/')
        self.assertEqual(response.status_code, 200)
        # accroding to code should redirect to index?
        #redirect = "mammals/login/"
        #self.assertRedirects(response, redirect)
        #self.assertTemplateUsed('mammals/index.html')

    # def test_gridblock_post(self):
    #     response = self.c.post('/mammals/grid_square/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed('mammals/grid_block.html')


    #(r'^grid/$', 'blackrock.mammals.views.grid'),
    def test_grid_get(self):
        #only has code to deal with post... dont think that will matter much...
        response = self.c.get('/mammals/grid/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid.html')

    def test_grid_post(self):
        #only has code to deal with post... dont think that will matter much...
        response = self.c.post('/mammals/grid/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid.html')


    # (r'^grid_square_csv/$',     'blackrock.mammals.views.grid_square_csv'),
    # def test_grid_square_csv(self):
    #     response = self.c.post('/mammals/grid_square_csv/')
    #     self.assertEqual(response.status_code, 200)




    # (r'^grid_square_print/$',     'blackrock.mammals.views.grid_square_print'),
    # def test_grid_square_print(self):

    # (r'^sandbox/$',     'blackrock.mammals.views.sandbox_grid'),
    def test_sandbox_get(self):
        response = self.c.get('/mammals/sandbox/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/sandbox_grid.html')

    def test_sandbox_post(self):
        response = self.c.post('/mammals/sandbox/', {"height_in_blocks" : 15, "width_in_blocks" : 15, "block_size_in_m": 15, "grid_center_y": 15, "grid_center_x" : 15})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/sandbox_grid.html')

    # (r'^sandbox/grid/$',     'blackrock.mammals.views.sandbox_grid'),
    def test_sandbox_grid_post(self):
        response = self.c.post('/mammals/sandbox/grid/', {"height_in_blocks" : 15, "width_in_blocks" : 15, "block_size_in_m": 15, "grid_center_y": 15, "grid_center_x" : 15})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/sandbox_grid.html')

    def test_sandbox_grid_post_block_size_less_than_ten(self):
        response = self.c.post('/mammals/sandbox/grid/', {"height_in_blocks" : 15, "width_in_blocks" : 15, "block_size_in_m": 5, "grid_center_y": 15, "grid_center_x" : 15})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/sandbox_grid.html')


    def test_sandbox_grid_get(self):
        response = self.c.post('/mammals/sandbox/grid/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/sandbox_grid.html')

    # (r'^sandbox/grid_square/$',     'blackrock.mammals.views.sandbox_grid_block'),
    def test_sandbox_grid_square_get(self):
        response = self.c.get('/mammals/sandbox/grid_square/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid_block.html')

    def test_sandbox_grid_square_post(self):
        response = self.c.post('/mammals/sandbox/grid_square/', {"num_transects" : 15, "points_per_transect" : 15, "agnetic_declination" : 15, "block_size_in_m" : 15, "selected_block_center_y" : 15, "selected_block_center_x" : 15, "grid_center_y" : 15, "grid_center_x" : 15, "height_in_blocks" : 15, "width_in_blocks" : 15 })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid_block.html')

    def test_sandbox_grid_square_post_num_trans_greater_than_twenty(self):
        response = self.c.post('/mammals/sandbox/grid_square/', {"num_transects" : 30, "points_per_transect" : 15, "agnetic_declination" : 15, "block_size_in_m" : 15, "selected_block_center_y" : 15, "selected_block_center_x" : 15, "grid_center_y" : 15, "grid_center_x" : 15, "height_in_blocks" : 15, "width_in_blocks" : 15 })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid_block.html')

    def test_sandbox_grid_square_post_points_per_transect_less_than_4(self):
        response = self.c.post('/mammals/sandbox/grid_square/', {"num_transects" : 15, "points_per_transect" : 2, "agnetic_declination" : 15, "block_size_in_m" : 15, "selected_block_center_y" : 15, "selected_block_center_x" : 15, "grid_center_y" : 15, "grid_center_x" : 15, "height_in_blocks" : 15, "width_in_blocks" : 15 })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('mammals/grid_block.html')

    # def test_process_save_team_form_get(request):
    #     response = self.c.get()
    #        if request.method != 'POST':
    #     return HttpResponseRedirect('/mammals/all_expeditions/')



    # (r'^logout/$', 'django.contrib.auth.views.logout',     {'next_page': '/mammals/'}), #requires permissions
    # (r'^all_expeditions/$',     'blackrock.mammals.views.all_expeditions'), #requires permissions
    # (r'^new_expedition_ajax/$',     'blackrock.mammals.views.new_expedition_ajax'),  #requires permissions
    # (r'^expedition/(?P<expedition_id>\d+)/$',     'blackrock.mammals.views.expedition'), #requires permissions
    # (r'^edit_expedition/(?P<expedition_id>\d+)/$',     'blackrock.mammals.views.edit_expedition'), #requires permissions
    # (r'^edit_expedition_ajax/$',     'blackrock.mammals.views.edit_expedition_ajax'), #requires permissions
    # (r'^sightings/$', 'blackrock.mammals.views.sightings'), #requires permissions
    # (r'^create_sighting/$',     'blackrock.mammals.views.create_sighting'), #requires permissions
    # (r'^sighting/(?P<sighting_id>\d+)/$',     'blackrock.mammals.views.sighting'), #requires permissions
    # (r'^edit_sighting/$',     'blackrock.mammals.views.edit_sighting'), #requires permissions
    # (r'^expedition/(?P<expedition_id>\d+)/animals/$',     'blackrock.mammals.views.expedition_animals'), #requires permissions
    # (r'^save_expedition_animals/$',     'blackrock.mammals.views.save_expedition_animals'), #requires permissions
    # (r'^team_form/(?P<expedition_id>\d+)/(?P<team_letter>\w+)/$',     'blackrock.mammals.views.team_form'), #requires permissions
    # (r'^save_team_form/$',     'blackrock.mammals.views.save_team_form'), 
    # (r'^save_team_form_ajax/$',     'blackrock.mammals.views.save_team_form_ajax'),  #requires permissions

    # url(r'^search/',
    #     MammalSearchView(template="mammals/search.html",
    #                      form_class=MammalSearchForm), name='search'),

    # url(r'^ajax_search/$',
    #     'blackrock.mammals.search.ajax_search'),

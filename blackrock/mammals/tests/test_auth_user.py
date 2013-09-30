# from django.test import TestCase, RequestFactory
# from django.test.client import Client
# from django.contrib.auth.models import User, Group
# from blackrock.mammals.views import process_login, index, grid_block
# from django.http import HttpResponse, HttpResponseRedirect
# from blackrock.mammals.models import *


# class AuthUserViewTest(TestCase):

#     def setUp(self):
#         '''Set up method for testing views.'''
#         self.factory = RequestFactory()
#         #self.group = Group.objects.get(name="mammals_module_data_entry")
#         self.user = User.objects.create_user('new_user', 'email@email.com', 'new_user')
#         self.user.whether_this_user_can_see_mammals_module_data_entry = 1
#         #elf.user.user_permissions.add(blackrock.mammals.models.whether_this_user_can_see_mammals_module_data_entry)
#         #self.group.user_set.add(self.user)
#         #self.group.save()
#         self.user.save()

# #tests to see if user has a permission called 'myModule' which is not 'myModule.view_myThing'
# #self.assertTrue(self.user.has_module_perms('myModule'))


#     def test_index(self):
#         response = self.user.get('/')
#         self.assertEqual(response.status_code, 302)
#         self.assertTemplateUsed('mammals/index.html')
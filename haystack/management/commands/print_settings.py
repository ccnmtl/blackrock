import sys
from django.core.management.base import NoArgsCommand
from django.template import loader, Context
from haystack.constants import DEFAULT_OPERATOR


class Command(NoArgsCommand):
    help = "Generates a Solr schema that reflects the indexes."
    
    def handle_noargs(self, **options):
        """Generates a Solr schema that reflects the indexes."""
        # Cause the default site to load.
        from django.conf import settings
        from haystack import backend, site
        search_backend = backend.SearchBackend()
        #import pdb
        #pdb.set_trace()
        print "solr path"
        print search_backend.conn.url
        print search_backend.conn.base_url
        print search_backend.conn.path
        print "registered models "
        print search_backend.build_registered_models_list()
        print "search fields"
        print search_backend.site.all_searchfields().keys()
        print "indexed models"
        print search_backend.site.get_indexed_models()

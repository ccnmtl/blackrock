from django import template
from django.utils.text import capfirst
from haystack.query import SearchQuerySet
register = template.Library()
from django.conf import settings
import types

    
    

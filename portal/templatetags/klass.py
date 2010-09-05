from django import template
from django.utils.text import capfirst
register = template.Library()

@register.filter('klass')
def klass(obj):
    return obj._meta.object_name
  
@register.filter('klass_display')
def klass_display(obj):
    return capfirst(obj._meta.verbose_name)
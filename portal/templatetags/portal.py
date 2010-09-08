from django import template
from django.utils.text import capfirst
register = template.Library()

@register.filter('klass')
def klass(obj):
    return obj._meta.object_name
  
@register.filter('klass_display')
def klass_display(obj):
    return capfirst(obj._meta.verbose_name)
  
@register.filter('infrastructure')
def infrastructure(obj):
    return [facet.display_name for facet in obj.facet.filter(facet='Infrastructure')]
  
@register.filter('detail_url')
def detail_url(obj):
    if obj._meta.object_name == 'ForestStory':
      url = "/portal/foreststories/%s/" % (obj.name) 
    else:
      url = "/portal/browse/portal/%s/objects/%s" % (obj._meta.object_name.lower(), obj.id)
      
    return url
    
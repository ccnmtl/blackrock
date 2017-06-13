from django import template
from djangohelpers.templatetags import TemplateTagNode

register = template.Library()


class GetBreakdownCount(TemplateTagNode):

    noun_for = {
        'id_within_facet': 'id_within_facet',
        'for_facet': 'facet',
        'with_breakdown': 'breakdown'
    }

    def __init__(self, varname, id_within_facet, facet, breakdown):
        TemplateTagNode.__init__(self, varname,
                                 id_within_facet=id_within_facet,
                                 facet=facet, breakdown=breakdown)

    def execute_query(self, id_within_facet, facet, breakdown):
        return 'hi'


register.tag('get_breakdown_count', GetBreakdownCount.process_tag)

"""{% load mammals_templatetags %}
{% get_breakdown_count id_within_facet 12 with_breakdown 123
for_facet 123  as the_breakdown %} {{ the_breakdown }}
"""

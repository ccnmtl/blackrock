from django import template
from djangohelpers.templatetags import TemplateTagNode

from blackrock.mammals.models import *
import pdb


register = template.Library()


class GetBreakdownCount(TemplateTagNode):
    
    noun_for = {
       'id_within_facet' : 'id_within_facet'
       ,'for_facet':     'facet'
       ,'with_breakdown': 'breakdown'
    }

    def __init__(self, varname, id_within_facet, facet, breakdown):
        TemplateTagNode.__init__(self, varname, id_within_facet=id_within_facet, facet=facet, breakdown=breakdown)

    def execute_query(self, id_within_facet, facet, breakdown):
        print 'hi HIIIIIIIIIII'
        return 'hi'
        
register.tag('get_breakdown_count', GetBreakdownCount.process_tag)

"""{% load mammals_templatetags %}
{% get_breakdown_count id_within_facet 12 with_breakdown 123  for_facet 123  as the_breakdown %} {{ the_breakdown }}
"""


if 1 == 0:
            class GetAnswer(TemplateTagNode):
                
                noun_for = {
                   'of_family': 'family_id',
                   'to_question': 'display_question_id'
                }

                def __init__(self, varname, display_question_id, family_id):
                    TemplateTagNode.__init__(self, varname, display_question_id=display_question_id, family_id=family_id)

                def execute_query(self, display_question_id, family_id):
                    f = Family.objects.get (pk = family_id)
                    q = DisplayQuestion.objects.get (pk = display_question_id).question
                    responses =  Response.objects.filter (family =f, question = q )
                    if responses.count() == 0:
                      return None
                    return list (responses)[-1]
                    
            register.tag('get_answer', GetAnswer.process_tag)


            def get_goal_info (family, goal_number):
              try:
                return family.goal_info.values() [goal_number]
              except:
                return {}

            class GetGoalInfo1(TemplateTagNode):
                noun_for = { 'of_family': 'family_id'}
                def __init__(self, varname, family_id):
                    TemplateTagNode.__init__(self, varname, family_id=family_id)
                def execute_query(self,  family_id):
                    f = Family.objects.get (pk = family_id)
                    return get_goal_info (f, 0)
            register.tag('get_goal_info_1', GetGoalInfo1.process_tag)
                
            class GetGoalInfo2(TemplateTagNode):
                noun_for = { 'of_family': 'family_id'}
                def __init__(self, varname, family_id):
                    TemplateTagNode.__init__(self, varname, family_id=family_id)
                def execute_query(self,  family_id):
                    f = Family.objects.get (pk = family_id)
                    return get_goal_info (f, 1)
            register.tag('get_goal_info_2', GetGoalInfo2.process_tag)

            class GetGoalInfo3(TemplateTagNode):
                noun_for = { 'of_family': 'family_id'}
                def __init__(self, varname, family_id):
                    TemplateTagNode.__init__(self, varname, family_id=family_id)
                def execute_query(self,  family_id):
                    f = Family.objects.get (pk = family_id)
                    return get_goal_info (f, 2)
            register.tag('get_goal_info_3', GetGoalInfo3.process_tag)


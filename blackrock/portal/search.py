from django import forms
from django.db.models import get_model
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.views import SearchView
from blackrock.portal.models import Facet
from types import ListType


def default_type_choices(site=None):
    return [('DataSet', 'Data Set'),
            ('ForestStory', 'Forest Story'),
            ('LearningActivity', 'Learning Activity'),
            ('Person', 'Person'),
            ('ResearchProject', 'Research Project'),
            ('Sighting', 'Sighting'),
            ('Station', 'Station'),
            ('TrapLocation', 'Trap Location')]


def default_facet_choices(facet):

    choices = [(f.name, f.display_name)
               for f in Facet.objects.filter(facet=facet)]
    choices.sort()
    return choices


class PortalSearchForm(SearchForm):

    asset_type = forms.MultipleChoiceField(
        required=False, label=_('Record Type'),
        widget=forms.CheckboxSelectMultiple, choices=default_type_choices())

    study_type = forms.MultipleChoiceField(
        required=False, label=_('Study Type'),
        widget=forms.CheckboxSelectMultiple,
        choices=default_facet_choices("Study Type"))

    species = forms.MultipleChoiceField(
        required=False,
        label=_('Species'),
        widget=forms.CheckboxSelectMultiple,
        choices=default_facet_choices("Species"))

    discipline = forms.MultipleChoiceField(
        required=False,
        label=_('Discipline'),
        widget=forms.CheckboxSelectMultiple,
        choices=default_facet_choices("Discipline"))

    def __init__(self, *args, **kwargs):
        super(PortalSearchForm, self).__init__(*args, **kwargs)

    def get_multiplechoicefield(self, name):
        query = ""

        if hasattr(self, "cleaned_data"):
            if name in self.cleaned_data:
                for a in self.cleaned_data[name]:
                    if len(query):
                        query += ' OR '
                    query += "%s:%s" % (name, a)
        return query

    def search(self):
        sqs = []
        self.hidden = []

        if self.is_valid():
            q = self.cleaned_data['q'].lower()

            if len(q) == 0:
                sqs = self.searchqueryset.all()
            else:
                sqs = self.searchqueryset.auto_query(q, fieldname="text")

            if self.load_all:
                sqs = sqs.load_all()

            for facet in Facet.asset_facets:
                sqs = sqs.facet(facet)
                if facet in self.fields:
                    self.fields[facet].choices = []

            for facet in Facet.asset_facets:
                query = self.get_multiplechoicefield(facet)
                if len(query):
                    sqs = sqs.narrow(query)

        # facet counts based on result set
        if len(sqs) > 0:  # ## this is broken
            counts = sqs.facet_counts()
            for facet in counts['fields']:
                if facet in self.fields:
                    for key, value in counts['fields'][facet]:
                        if value > 0:
                            # Look up the display name for this facet
                            display_name = key
                            try:
                                x = Facet.objects.get(name=key)
                                display_name = x.display_name
                            except:
                                model = get_model("portal", key)
                                if model:
                                    display_name = capfirst(
                                        model._meta.verbose_name)

                            choice = (key, "%s (%s)" % (display_name, value))
                            self.fields[facet].choices.append(choice)

                    self.fields[facet].choices.sort()

        return sqs


class PortalSearchView(SearchView):

    def extra_context(self):
        extra = super(PortalSearchView, self).extra_context()
        if hasattr(self, "results"):
            if type(self.results) is ListType and len(self.results) < 1:
                extra["count"] = -1
            else:
                extra["count"] = len(self.results)

        # Send down our current parameters minus page number
        query = ''
        for param, value in self.request.GET.items():
            if param != 'page':
                query += '%s=%s&' % (param, value)
        extra['query'] = query
        return extra

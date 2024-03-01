from django import forms
from django.apps import apps
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
from haystack.forms import SearchForm
from haystack.views import SearchView
from blackrock.portal.models import Facet


def default_type_choices(site=None):
    return [('DataSet', 'Data Set'),
            ('ForestStory', 'Forest Story'),
            ('LearningActivity', 'Learning Activity'),
            ('Person', 'Person'),
            ('ResearchProject', 'Research Project'),
            ('Sighting', 'Sighting'),
            ('Station', 'Station')]


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
        widget=forms.CheckboxSelectMultiple)

    species = forms.MultipleChoiceField(
        required=False,
        label=_('Species'),
        widget=forms.CheckboxSelectMultiple)

    discipline = forms.MultipleChoiceField(
        required=False,
        label=_('Discipline'),
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(PortalSearchForm, self).__init__(*args, **kwargs)
        self.fields['study_type'].choices = default_facet_choices(
            "Study Type")
        self.fields['species'].choices = default_facet_choices("Species")
        self.fields['discipline'].choices = default_facet_choices("Discipline")

    def get_multiplechoicefield(self, name):
        query = ""

        if hasattr(self, "cleaned_data"):
            if name in self.cleaned_data:
                for a in self.cleaned_data[name]:
                    if len(query):
                        query += ' OR '
                    query += "%s:%s" % (name, a)
        return query

    def _get_sqs(self):
        sqs = []
        self.hidden = []

        if not self.is_valid():
            return sqs

        q = self.cleaned_data['q'].lower()

        if len(q) == 0:
            sqs = self.searchqueryset.all()
        else:
            sqs = self.searchqueryset.auto_query(q, fieldname="text")

        sqs = self.sqs_load_all(sqs)

        for facet in Facet.asset_facets:
            sqs = sqs.facet(facet)
            if facet in self.fields:
                self.fields[facet].choices = []

        for facet in Facet.asset_facets:
            query = self.get_multiplechoicefield(facet)
            if len(query):
                sqs = sqs.narrow(query)
        return sqs

    def sqs_load_all(self, sqs):
        if self.load_all:
            return sqs.load_all()
        return sqs

    def search(self):
        sqs = self._get_sqs()

        # facet counts based on result set
        if len(sqs) <= 0:
            return sqs

        self.update_facets(sqs)

        return sqs

    def update_facets(self, sqs):
        counts = sqs.facet_counts()
        for facet in counts['fields']:
            if facet not in self.fields:
                continue

            for key, value in counts['fields'][facet]:
                if value > 0:
                    display_name = get_facet_display_name(key)
                    choice = (key, "%s (%s)" % (display_name, value))
                    self.fields[facet].choices.append(choice)

            self.fields[facet].choices.sort()


def get_facet_display_name(key):
    # Look up the display name for this facet
    display_name = key
    try:
        x = Facet.objects.get(name=key)
        display_name = x.display_name
    except Facet.DoesNotExist:
        try:
            model = apps.get_model("portal", key)
            if model:
                display_name = capfirst(
                    model._meta.verbose_name)
        except LookupError:
            pass
    return display_name


class PortalSearchView(SearchView):

    def extra_context(self):
        extra = super(PortalSearchView, self).extra_context()
        if hasattr(self, "results"):
            if isinstance(self.results, list) and len(self.results) < 1:
                extra["count"] = -1
            else:
                extra["count"] = len(self.results)

        # Send down our current parameters minus page number
        query = ''
        for param, value in list(self.request.GET.items()):
            if param != 'page':
                query += '%s=%s&' % (param, value)
        extra['query'] = query
        return extra

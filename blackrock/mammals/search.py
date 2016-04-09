from blackrock.mammals.models import Species, Habitat, School, GridSquare
from collections import defaultdict
from datetime import datetime
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
from haystack.forms import SearchForm
from haystack.views import SearchView
from types import ListType


def my_counter(L):
    d = defaultdict(int)
    for i in L:
        d[i] += 1
    return d


class MammalSearchForm(SearchForm):

    success_list = [
        ('unsuccessful', 'Unsuccessful traps'), (
            'trapped_and_released', 'Trapped and released')
    ]

    signs_list = [
        ('observed', 'Observed'),
        ('camera', 'Camera'),
        ('tracks_and_signs', 'Tracks and signs')
    ]

    csm = forms.CheckboxSelectMultiple
    # note: the order in which these are defined... affects the order in which
    # they are displayed in the template. This sucks but it's what I get for
    # accepting to use Django forms.

    success = forms.MultipleChoiceField(
        required=False, label='', widget=csm, choices=success_list)
    signs = forms.MultipleChoiceField(
        required=False, label='', widget=csm, choices=signs_list)
    habitat = forms.MultipleChoiceField(
        required=False, label='Habitat', widget=csm)
    species = forms.MultipleChoiceField(
        required=False, label='Species', widget=csm)
    school = forms.MultipleChoiceField(
        required=False, label='School', widget=csm)

    from_date = forms.CharField(
        required=False, initial="start date", max_length=10,
        help_text='Click to select a start date for your search')
    until_date = forms.CharField(
        required=False, initial="end date", max_length=10,
        help_text='Click to select an end date for your search.')

    def __init__(self, *args, **kwargs):
        super(MammalSearchForm, self).__init__(*args, **kwargs)
        habitat_list = [(h.id, h.label) for h in Habitat.objects.all()]
        species_list = [(s.id, s.common_name) for s in Species.objects.all()]
        school_list = [(s.id, s.name) for s in School.objects.all()]
        self.fields['habitat'].choices = habitat_list
        self.fields['species'].choices = species_list
        self.fields['school'].choices = school_list

    def checkboxes_or(self, form_key):
        """" note: this returns a blank string if nothing is checked."""
        search_index_key = form_key
        if form_key == 'species':
            search_index_key = 'species_id'
        return ' OR '.join(['%s:%s' % (search_index_key, a)
                            for a in self.cleaned_data[form_key]])

    def calculate_breakdown(self, the_sqs):
        result = {}
        for thing in ['species_id', 'habitat', 'school', 'unsuccessful',
                      'trapped_and_released', 'observed',
                      'camera', 'tracks_and_signs']:
            what_to_count = [getattr(x, ('%s' % thing)) for x in the_sqs]
            if thing == 'species_id':
                result['species'] = my_counter(what_to_count)
            else:
                result[thing] = my_counter(what_to_count)

        result['success'] = {}
        result['success']['unsuccessful'] = result[
            'trapped_and_released'][False]
        result['success']['trapped_and_released'] = result[
            'trapped_and_released'][True]

        result['signs'] = {}
        result['signs']['observed'] = result['observed'][True]
        result['signs']['camera'] = result[
            'camera'][True]
        result['signs']['tracks_and_signs'] = result[
            'tracks_and_signs'][True]

        return result

    def basic_results(self):
        sqs = self.searchqueryset.auto_query('')
        sqs = sqs.narrow(
            'asset_type_exact:TrapLocation OR asset_type_exact:Sighting')
        # don't display fake/test results:
        sqs = sqs.narrow('real_exact:True')
        return sqs

    def search(self):
        sqs = []
        self.hidden = []

        if self.is_valid():
            # else
            # TODO test validity of connection to the stupid SOLR server
            # and throw some kind of error if there's a problem.
            # note -- haystack catches the error. so i can't. This kinda sucks.

            sqs = self.basic_results()

            # hack:
            for aaa in sqs:
                aaa.species = aaa.species_id

            sqs = sqs.narrow(self.checkboxes_or('habitat'))
            sqs = sqs.narrow(self.checkboxes_or('species'))
            sqs = sqs.narrow(self.checkboxes_or('school'))

            from_date_val, until_date_val = None, None
            we_have_dates = False

            try:
                from_date_val = datetime.strptime(
                    self.cleaned_data['from_date'], '%m/%d/%Y')
                until_date_val = datetime.strptime(
                    self.cleaned_data['until_date'], '%m/%d/%Y')
                if not from_date_val < until_date_val:
                    raise ValueError(
                        "The first date should be before the second date.")
                we_have_dates = True
            except ValueError:
                pass  # we don't have dates but I don't really care.

            if we_have_dates:
                when = (from_date_val.strftime('%Y-%m-%d'),
                        until_date_val.strftime('%Y-%m-%d'))
                sqs = sqs.narrow(
                    'date:[%sT00:00:00.000Z TO %sT23:59:59.999Z]' % when)

            sqs = self.trap_success(sqs)
        else:
            sqs = self.basic_results()

        self.breakdown = dumps(self.calculate_breakdown(sqs))
        return sqs

    def trap_success(self, sqs):
        # trap success:
        show_unsuccessful = 'unsuccessful' in self.cleaned_data[
            'success']
        show_successful = 'trapped_and_released' in self.cleaned_data[
            'success']
        observed = 'observed' in self.cleaned_data[
            'signs']
        camera = 'camera' in self.cleaned_data[
            'signs']
        tracks_and_signs = 'tracks_and_signs' in self.cleaned_data[
            'signs']
        if (observed or camera or tracks_and_signs or
                show_unsuccessful or show_successful):
            tmp = []
            if observed:
                tmp.append('observed:True')
            if camera:
                tmp.append('camera:True')
            if tracks_and_signs:
                tmp.append('tracks_and_signs:True')
            if show_unsuccessful:
                tmp.append('unsuccessful:True')
            if show_successful:
                tmp.append('trapped_and_released:True')
            return sqs.narrow(' OR '.join(tmp))
        return sqs


class MammalSearchView(SearchView):

    def __init__(self, *args, **kwargs):
        hella_many = 5000000000
        super(MammalSearchView, self).__init__(*args, **kwargs)
        self.results_per_page = hella_many

    def extra_context(self):
        """ this only gets run the first time we load the page."""
        # print "Extra context"
        extra = super(MammalSearchView, self).extra_context()
        if hasattr(self, "results"):
            if type(self.results) is ListType and len(self.results) < 1:
                extra["count"] = -1
            else:
                extra["count"] = len(self.results)
        query = ''
        for param, value in self.request.GET.items():
            if param != 'page':
                query += '%s=%s&' % (param, value)

        grid = [gs.info_for_display()
                for gs in GridSquare.objects.all() if gs.display_this_square]
        extra['grid_json'] = dumps(grid)
        extra['query'] = query
        extra['little_habitat_disks_json'] = dumps(
            dict((a.id, a.image_path_for_legend)
                 for a in Habitat.objects.all()))
        extra['habitat_colors_json'] = dumps(
            dict((a.id, a.color_for_map) for a in Habitat.objects.all()))

        if not hasattr(self.form, 'breakdown'):
            self.form.breakdown = {}

        extra['results_json'] = dumps(
            [search_map_repr(tl) for tl in self.results])
        return extra


def ajax_search(request):
    if request.method == 'POST':
        my_new_form = MammalSearchForm(request.POST)
        search_results = my_new_form.search()
        result_obj = {}
        result_obj['map_data'] = [
            search_map_repr(tl) for tl in search_results]
        result_obj['breakdown_object'] = my_new_form.calculate_breakdown(
            search_results)
        return HttpResponse(dumps(result_obj))
    else:
        return HttpResponseRedirect('/mammals/search/')


# TODO what happens if lat or long is NULL?
def search_map_repr(obj):

    result = {}
    html_string = """
        Animal: %s</br>
        Habitat: %s</br>
        School: %s</br>
        Observer(s): %s</br>
        Date: %s"""

    vals = (
        obj.species_label,
        obj.habitat_label,
        obj.school_label,
        obj.observer_name,
        obj.date
    )

    result['name'] = html_string % vals

    try:
        result['where'] = [float(obj.lat), float(obj.lon)]
    except TypeError:
        result['where'] = [0.0, 0.0]

    result['species'] = obj.species_label
    result['habitat_id'] = obj.habitat
    result['habitat'] = obj.habitat_label
    result['school_id'] = obj.school
    result['school'] = obj.school
    result['school_label'] = obj.school_label

    if obj.date is not None:
        result['date'] = obj.date.strftime("%m/%d/%y")
    else:
        result['date'] = ''

    return result

from datetime import datetime
from django import forms
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.db.models import Manager
from django.db.models.signals import pre_save
from pagetree.models import PageBlock
import re


MAX_DISPLAY_LENGTH = 50


# Static Lookup Tables
class Audience(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DigitalFormat(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def is_image(self):
        return self.name in ['png', 'jpg', 'gif', 'bmp']

    def is_video(self):
        return self.name in ['mp4', 'flv', 'm4v']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Facet(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100)
    facet = models.CharField(max_length=50)

    asset_facets = ['study_type', 'species', 'discipline',
                    'asset_type', 'infrastructure']

    class Meta:
        unique_together = (("name", "facet"),)
        ordering = ['display_name']

    def __str__(self):
        return self.display_name

    def solr_name(self):
        return self.facet.replace(' ', '_').lower()


class Institution(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LocationSubtype(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LocationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PersonType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PublicationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RegionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RightsType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Url(models.Model):
    name = models.URLField()
    display_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def document(self):
        a = self.name.split("/")
        return a[len(a) - 1]


# Base Assets
class DigitalObject(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    digital_format = models.ForeignKey(DigitalFormat, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="portal/%Y/%m/%d/", null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=500, null=True, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    facet = models.ManyToManyField(Facet)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    markup = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Digital Object"
        ordering = ['name']


class Location(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    location_type = models.ManyToManyField(LocationType, blank=True)
    location_subtype = models.ManyToManyField(
        LocationSubtype, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=10)
    longitude = models.DecimalField(max_digits=18, decimal_places=10)
    latlong = models.PointField(null=True, blank=True)
    objects = Manager()

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def __str__(self):
        return "%s (%.6f,%.6f)" % (self.name, self.latitude, self.longitude)

    class Meta:
        ordering = ['name']


def update_location_geometry(sender, **kwargs):
    obj = kwargs['instance']
    obj.latlong = "POINT(%s %s)" % (obj.latitude, obj.longitude)


pre_save.connect(update_location_geometry, sender=Location)


class Station(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    access_means = models.TextField(null=True, blank=True)
    activation_date = models.DateField('activation_date')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    digital_object = models.ManyToManyField(
        DigitalObject, blank=True,
        related_name="station_digital_object")  # for extra images & resources
    facet = models.ManyToManyField(Facet)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def related_ex(self):
        extra = []
        extra.extend(self.datasets())
        extra.extend(self.research_projects())
        return extra

    def research_projects(self):
        assets = []
        for d in self.datasets():
            for p in d.researchproject_set.all():
                assets.append(p)
        return assets

    def datasets(self):
        assets = []
        if self.location:
            for p in self.location.dataset_set.all():
                assets.append(p)
        return assets

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Station"
        verbose_name_plural = "Stations"


class Region(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    location = models.ManyToManyField(Location, blank=True)
    region_type = models.ManyToManyField(RegionType)

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def research_projects(self):
        assets = []
        for loc in self.location.all():
            for p in loc.researchproject_set.all():
                assets.append(p)
        return assets

    def learning_activities(self):
        assets = []
        for loc in self.location.all():
            for p in loc.learningactivity_set.all():
                assets.append(p)
        return assets

    def datasets(self):
        assets = []
        for loc in self.location.all():
            for p in loc.dataset_set.all():
                assets.append(p)
        return assets

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    full_name = models.CharField(max_length=500)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    person_type = models.ManyToManyField(PersonType)
    institution = models.ManyToManyField(Institution)
    professional_title = models.CharField(
        max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)

    def name(self):
        if len(self.first_name) > 0:
            return "%s, %s" % (self.last_name, self.first_name)
        else:
            return self.last_name

    def display_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Person"
        verbose_name_plural = "People"


class DataSet(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    collection_start_date = models.DateField()
    collection_end_date = models.DateField(null=True, blank=True)
    rights_type = models.TextField(default="open")
    url = models.ManyToManyField(Url, blank=True)
    spatial_explicit = models.BooleanField(default=False)
    blackrock_id = models.CharField(
        max_length=50, unique=True, null=True, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    person = models.ManyToManyField(Person, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def __str__(self):
        return self.name

    def station(self):
        if len(self.location.station_set.all()) < 1:
            return None
        else:
            return self.location.station_set.all()[0]

    class Meta:
        verbose_name = "Data Set"
        ordering = ['name']


class Publication(models.Model):
    name = models.CharField(max_length=500, unique=True)
    citation = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    publication_type = models.ManyToManyField(
        PublicationType, blank=True)
    rights_type = models.ManyToManyField(RightsType)
    url = models.URLField(null=True, blank=True)
    doi_citation = models.TextField(null=True, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    display_image = models.ForeignKey(DigitalObject, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    person = models.ManyToManyField(Person, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def __str__(self):
        if len(self.name) > 25:
            return "%s..." % self.name[0:25]
        else:
            return self.name

    class Meta:
        ordering = ['name']


class ResearchProject(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    dataset = models.ManyToManyField(DataSet, blank=True)
    digital_object = models.ManyToManyField(
        DigitalObject, blank=True)
    display_image = models.ForeignKey(
        DigitalObject, null=True, blank=True,
        related_name="researchproject_display_image",
        on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    location = models.ForeignKey(Location, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    person = models.ManyToManyField(Person, blank=True)
    publication = models.ManyToManyField(Publication, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    def __str__(self):
        if len(self.name) > MAX_DISPLAY_LENGTH:
            return "%s..." % self.name[0:MAX_DISPLAY_LENGTH]
        else:
            return self.name

    class Meta:
        verbose_name = "Research Project"
        ordering = ['name']

    def related_ex(self):
        extra = []
        extra.extend(self.dataset.all())
        return extra


class LearningActivity(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    author = models.ManyToManyField(Person, related_name="author")
    digital_format = models.ManyToManyField(DigitalFormat)
    url = models.ManyToManyField(Url, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    dataset = models.ManyToManyField(DataSet, blank=True)
    digital_object = models.ManyToManyField(
        DigitalObject, blank=True)
    display_image = models.ForeignKey(
        DigitalObject, null=True, blank=True,
        related_name="learningactivity_display_image",
        on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    location = models.ForeignKey(Location, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    person = models.ManyToManyField(Person, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    class Meta:
        verbose_name = "Learning Activity"
        verbose_name_plural = "Learning Activities"
        ordering = ['name']

    def __str__(self):
        return self.name

    def related_ex(self):
        extra = []
        extra.extend(self.dataset.all())
        extra.extend(self.person.all())
        return extra


class ForestStory(models.Model):
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to="portal/%Y/%m/%d/", null=True, blank=True)
    url = models.ManyToManyField(Url, blank=True)

    audience = models.ManyToManyField(Audience, blank=True)
    dataset = models.ManyToManyField(DataSet, blank=True)
    digital_object = models.ManyToManyField(
        DigitalObject, blank=True)
    display_image = models.ForeignKey(
        DigitalObject, null=True, blank=True,
        related_name="foreststory_display_image",
        on_delete=models.SET_NULL)
    facet = models.ManyToManyField(Facet)
    learning_activity = models.ManyToManyField(
        LearningActivity, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    person = models.ManyToManyField(Person, blank=True)
    publication = models.ManyToManyField(Publication, blank=True)
    research_project = models.ManyToManyField(
        ResearchProject, blank=True)
    station = models.ManyToManyField(
        Station, blank=True,
        related_name="foreststory_related_station")
    tag = models.ManyToManyField(Tag, blank=True)

    created_date = models.DateTimeField('created_date', default=datetime.now)
    modified_date = models.DateTimeField('modified_date', default=datetime.now)

    class Meta:
        verbose_name = "Forest Story"
        verbose_name_plural = "Forest Stories"
        ordering = ['display_name']

    def __str__(self):
        return self.name

    def related_ex(self):
        extra = []
        extra.extend(self.station.all())
        extra.extend(self.learning_activity.all())
        extra.extend(self.research_project.all())
        extra.extend(self.dataset.all())
        return extra


class AssetList(models.Model):
    pageblocks = GenericRelation(
        PageBlock)
    search_criteria = models.TextField()
    template_file = "portal/assetlist.html"
    display_name = "Asset List"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return str(self.pageblock())

    def needs_submit(self):
        return False

    def list_count(self):
        return settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE

    @classmethod
    def add_form(self):
        return AssetListForm()

    def edit_form(self):
        return AssetListForm(instance=self)

    @classmethod
    def create(self, request):
        form = AssetListForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = AssetListForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def list(self):
        from haystack.query import SearchQuerySet

        results = SearchQuerySet()
        for facet in Facet.asset_facets:
            results = results.facet(facet)

        types = self.search_criteria.split(';')
        for t in types:
            criteria = t.split(',')
            q = ''
            for c in criteria:
                if len(q):
                    q += ' OR '
                q += c.strip()
            results = results.narrow(q)

        return results.order_by("name")

    def search_query(self):
        query = ''
        types = self.search_criteria.split(';')
        for t in types:
            criteria = t.split(',')
            for c in criteria:
                c = c.replace(':', '=')
                query += c.strip() + "&"

        return query

    def audience(self):
        try:
            m = re.search(r"audience:\w*", self.search_criteria)
            return m.group(0).split(":")[1].lower()
        except AttributeError:
            return None


class FeaturedAsset(models.Model):
    pageblocks = GenericRelation(
        PageBlock)
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    detailed_display = models.BooleanField(default=False)

    # pick one
    asset_location = models.ForeignKey(
        Location, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_station = models.ForeignKey(
        Station, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_region = models.ForeignKey(
        Region, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_person = models.ForeignKey(
        Person, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_digitalobject = models.ForeignKey(
        DigitalObject, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_publication = models.ForeignKey(
        Publication, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_dataset = models.ForeignKey(
        DataSet, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_research_project = models.ForeignKey(
        ResearchProject, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_learning_activity = models.ForeignKey(
        LearningActivity, null=True, blank=True,
        on_delete=models.SET_NULL)
    asset_forest_story = models.ForeignKey(
        ForestStory, null=True, blank=True,
        on_delete=models.SET_NULL)

    template_file = "portal/featuredasset.html"
    display_name = "Featured Asset"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return self.asset().name

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return FeaturedAssetForm()

    def edit_form(self):
        return FeaturedAssetForm(instance=self)

    @classmethod
    def create(self, request):
        form = FeaturedAssetForm(request.POST)
        if form.is_valid():
            return form.save()

    def edit(self, vals, files):
        form = FeaturedAssetForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def asset(self):
        # figure out which one is not null, and return it!
        for f in self._meta.fields:
            if 'asset_' in f.name:
                attr = self.__getattribute__(f.name)
                if attr:
                    return attr

    def save(self, *args, **kwargs):
        super(FeaturedAsset, self).save(*args, **kwargs)
        facet = Facet.objects.get(name="Featured " + self.audience.name)
        self.asset().facet.add(facet)
        self.asset().save()

    def delete(self):
        facet = Facet.objects.get(name="Featured " + self.audience.name)
        self.asset().facet.remove(facet)
        self.asset().save()
        super(FeaturedAsset, self).delete()  # Call the "real" save() method.

    def display_order(self):
        return self.pageblock.ordinality


class AssetListForm(forms.ModelForm):
    class Meta:
        model = AssetList
        exclude = ()


class FeaturedAssetForm(forms.ModelForm):
    class Meta:
        model = FeaturedAsset
        exclude = ()

    def clean(self):
        from django.core.exceptions import ValidationError
        # This should be forms.ValidationError. Need to do some work first to
        # get it that way

        asset_count = 0
        for field_name, val in list(self.cleaned_data.items()):
            if "asset_" in field_name and val is not None:
                asset_count += 1

        if asset_count == 0:
            raise ValidationError('Please select one object to display.')
        elif asset_count > 1:
            raise ValidationError('Please select only one object to display.')

        return self.cleaned_data


class PhotoGalleryItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    action = models.URLField()
    image = models.ForeignKey(DigitalObject, null=True, blank=True,
                              related_name="gallery_display_image",
                              on_delete=models.SET_NULL)
    position = models.IntegerField()

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.title


class PhotoGallery(models.Model):
    pageblocks = GenericRelation(
        PageBlock)
    template_file = "portal/photogallery.html"
    display_name = "Photo Gallery"
    item = models.ManyToManyField(PhotoGalleryItem, blank=True)

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return str(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return PhotoGalleryForm()

    def edit_form(self):
        return PhotoGalleryForm(instance=self)

    @classmethod
    def create(self, request):
        form = PhotoGalleryForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = PhotoGalleryForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()

    def current_time(self):
        today = datetime.today()
        minute = today.minute / 10 * 10

        return "%02d_%02d" % (today.hour, minute)


class PhotoGalleryForm(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        exclude = ()


class Webcam(models.Model):
    pageblocks = GenericRelation(
        PageBlock)
    template_file = "portal/webcam.html"
    display_name = "Webcam"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return str(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return WebcamForm()

    def edit_form(self):
        return WebcamForm(instance=self)

    @classmethod
    def create(self, request):
        form = WebcamForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = WebcamForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class WebcamForm(forms.ModelForm):
    class Meta:
        model = Webcam
        exclude = ()


class InteractiveMap(models.Model):
    pageblocks = GenericRelation(
        PageBlock)
    template_file = "portal/interactive_map.html"
    display_name = "Interactive Map"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __str__(self):
        return str(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return InteractiveMapForm()

    def edit_form(self):
        return InteractiveMapForm(instance=self)

    @classmethod
    def create(self, request):
        form = InteractiveMapForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = InteractiveMapForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class InteractiveMapForm(forms.ModelForm):
    class Meta:
        model = InteractiveMap
        exclude = ()


def get_all_related_objects(model):
    return [
        f for f in model._meta.get_fields()
        if (f.one_to_many or f.one_to_one)
        and f.auto_created and not f.concrete
        ]

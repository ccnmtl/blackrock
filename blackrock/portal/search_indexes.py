from haystack import indexes
from haystack.fields import MultiValueField, CharField
from blackrock.portal.models import Station, Person, DataSet, ForestStory, \
    ResearchProject, LearningActivity


class AssetIndex(indexes.SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField()
    study_type = MultiValueField(faceted=True)
    species = MultiValueField(faceted=True)
    discipline = MultiValueField(faceted=True)
    asset_type = CharField(faceted=True)
    infrastructure = MultiValueField(faceted=True)
    featured = MultiValueField(faceted=True)

    class Meta:
        abstract = True

    def prepare_study_type(self, obj):
        return [facet.name for facet in obj.facet.filter(facet='Study Type')]

    def prepare_species(self, obj):
        return [facet.name for facet in obj.facet.filter(facet='Species')]

    def prepare_discipline(self, obj):
        return [facet.name for facet in obj.facet.filter(facet='Discipline')]

    def prepare_infrastructure(self, obj):
        return [facet.name for facet in obj.facet.filter(
            facet='Infrastructure')]

    def prepare_asset_type(self, obj):
        return obj._meta.object_name

    def prepare_featured(self, obj):
        return [facet.name for facet in obj.facet.filter(facet='Featured')]

    def prepare_name(self, obj):
        return obj.name


class StationIndex(AssetIndex, indexes.Indexable):
    def get_model(self):
        return Station


class DataSetIndex(AssetIndex, indexes.Indexable):
    def get_model(self):
        return DataSet


class ResearchProjectIndex(AssetIndex, indexes.Indexable):
    def get_model(self):
        return ResearchProject


class LearningActivityIndex(AssetIndex, indexes.Indexable):
    def get_model(self):
        return LearningActivity


class ForestStoryIndex(AssetIndex, indexes.Indexable):
    def get_model(self):
        return ForestStory


class PersonIndex(AssetIndex, indexes.Indexable):
    def prepare_name(self, obj):
        return "%s, %s" % (obj.last_name, obj.first_name)

    def get_model(self):
        return Person

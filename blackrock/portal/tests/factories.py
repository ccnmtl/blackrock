import factory

from blackrock.portal.models import (
    Audience, Facet, Person, Region, AssetList, FeaturedAsset,
    PhotoGallery, Webcam, InteractiveMap, ForestStory)


class AudienceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Audience

    name = factory.Sequence(lambda n: "audience%03d" % n)


class FacetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facet

    name = "Sample Facet"
    display_name = "Sample Facet Display"
    facet = "a facet"


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    full_name = "John S. Doe"
    first_name = "John"
    last_name = "Doe"


class AssetListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssetList


class FeaturedAssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeaturedAsset


class PhotoGalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhotoGallery


class WebCamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Webcam


class InteractiveMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InteractiveMap


class ForestStoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ForestStory

import factory

from blackrock.portal.models import Audience, FeaturedAsset, Facet, Person


class AudienceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Audience

    name = "Sample Audience"


class FacetFactory(factory.DjangoModelFactory):
    class Meta:
        model = Facet

    name = "Sample Facet"
    display_name = "Sample Facet Display"
    facet = "a facet"


class FeaturedAssetFactory(factory.DjangoModelFactory):
    class Meta:
        model = FeaturedAsset

    audience = factory.SubFactory(AudienceFactory)


class PersonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Person

    full_name = "John S. Doe"
    first_name = "John"
    last_name = "Doe"

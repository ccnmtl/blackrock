import factory

from blackrock.portal.models import Audience, Facet, Person, Region


class AudienceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Audience

    name = factory.Sequence(lambda n: "audience%03d" % n)


class FacetFactory(factory.DjangoModelFactory):
    class Meta:
        model = Facet

    name = "Sample Facet"
    display_name = "Sample Facet Display"
    facet = "a facet"


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region


class PersonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Person

    full_name = "John S. Doe"
    first_name = "John"
    last_name = "Doe"

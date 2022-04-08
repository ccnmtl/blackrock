from django.db import models


# one "slice" of the core, containing multiple samples of pollen
class CoreSample(models.Model):
    def __str__(self):
        return str(self.depth)

    # in cm
    depth = models.DecimalField(max_digits=8, decimal_places=2)
    radiocarbon_years = models.IntegerField(default=0)


class PollenType(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.display_name

    POLLEN_TYPES = (
        ('A', 'Tree or shrub'),
        ('B', 'Herb'),
        ('F', 'Fern'),
        ('Q', 'Aquatic (water) plant'),
        ('S', 'Spore'),
    )

    type = models.CharField(max_length=1, choices=POLLEN_TYPES)
    display_name = models.CharField(max_length=100,
                                    null=False,
                                    unique=True,
                                    default="")


class PollenSample(models.Model):
    core_sample = models.ForeignKey(CoreSample, on_delete=models.CASCADE)
    pollen = models.ForeignKey(PollenType, on_delete=models.CASCADE)

    def __str__(self):
        return "%s cm: %s grains of %s (%s%%)" % (self.core_sample.depth,
                                                  self.count or 0,
                                                  self.pollen.name,
                                                  self.percentage or 0)

    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    count = models.DecimalField(max_digits=5, decimal_places=2, null=True)

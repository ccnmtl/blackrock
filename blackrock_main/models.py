from django.db import models

class LastImportDate(models.Model):
  application = models.CharField(max_length=50, unique=True)
  last_import = models.DateTimeField()

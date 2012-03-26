from django.db import models
from datetime import datetime
from pagetree.models import PageBlock, Section
from django.contrib.contenttypes import generic
from django import forms
from haystack.query import SearchQuerySet
from django.conf import settings
import re

from django.contrib.gis.db import models
from django.template import Context
from django.template.loader import get_template
from django.db.models.signals import pre_save
                            


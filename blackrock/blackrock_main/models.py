from django.db import models
from datetime import datetime
from pytz import timezone
import time
import pytz


class LastImportDate(models.Model):
    application = models.CharField(max_length=50, unique=True)
    last_import = models.DateTimeField()

    @classmethod
    def update_last_import_date(cls, application):
        dt = datetime.now()
        try:
            lid = LastImportDate.objects.get(application=application)
            lid.last_import = dt
        except LastImportDate.DoesNotExist:
            lid = LastImportDate.objects.create(
                application=application, last_import=datetime.now())
        lid.save()
        return dt

    @classmethod
    def _string_to_eastern_dst(cls, date_string, time_string):
        try:
            t = time.strptime(
                date_string + ' ' + time_string, '%Y-%m-%d %H:%M:%S')
            tz = pytz.timezone('US/Eastern')
            dt = datetime.datetime(
                t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=tz)
            return dt
        except:
            return None

    @classmethod
    def get_last_import_date(cls, dt, tm, application):
        last_import_date = cls._string_to_eastern_dst(dt, tm)

        if not last_import_date:
            try:
                last_import_date = LastImportDate.objects.get(
                    application=application).last_import
                last_import_date = last_import_date.replace(
                    tzinfo=timezone('US/Eastern'))
            except LastImportDate.DoesNotExist:
                pass

        return last_import_date

from django.core.management.base import BaseCommand
from django.db.models import get_model, get_app, get_models, ForeignKey, \
    OneToOneField, DateTimeField, DateField
from optparse import make_option
import datetime
import gdata.service
import gdata.spreadsheet
import gdata.spreadsheet.service
import sys
import time


class SpreadsheetColumn:
    attribute_name = None
    column_type = None
    value = None

    def get_type_name(self):
        if self.column_type:
            return self.column_type
        else:
            return self.attribute_name

    def get_entry_name(self):
        if self.column_type:
            return '%s.%s' % (self.attribute_name, self.column_type)
        else:
            return self.attribute_name


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--user', dest='user', help='GMail user id'),
        make_option('--pwd', dest='pwd', help='GMail password'),
        make_option('--sheet', dest='sheet', help='Spreadsheet name'),
        make_option('--app', dest='app', help='Django App')
    )

    def init_google_client(self, email, password):
        # initialize the spreadsheet service
        self.gd_client = gdata.spreadsheet.service.SpreadsheetsService()

        if (not email or email == ''):
            print "Please enter a valid email address"
            return False
        if (not password or password == ''):
            print "Please enter a valid password"
            return False

        # initialize the google library stuff
        self.gd_client.email = email
        self.gd_client.password = password
        self.gd_client.ProgrammaticLogin()
        return True

    def prepare_database(self, app_name):
        module = get_app(app_name)

        # Assumes models are in dependency order --
        # todo: anyway to do this without hard-coding?
        models = get_models(module)
        models.reverse()
        for m in models:
            m.objects.all().delete()

    def _parse_columns(self, map):
        columns = {}

        for k, v in map.items():
            c = SpreadsheetColumn()
            c.value = v.text
            a = k.split('.')
            if len(a) > 0:
                c.attribute_name = a[0]
                c.column_type = a[0]
            if len(a) > 1:
                c.column_type = a[1]

            columns[c.attribute_name] = c

        return columns

    def process_model_object(self, entry, model, app_name):
        try:
            opts = model._meta
            obj = model()  # bare model instance

            # list of columns, indexed by model attribute name.
            columns = self._parse_columns(entry.custom)

            # iterate the regular fields, these include everything but
            # many_to_many
            for field in opts.fields:
                # google spreadsheets strips spaces and underscores
                attribute_name = field.name.strip().replace('_', '')

                if attribute_name in columns.keys():
                    column = columns[attribute_name]
                    value = column.value

                    if value is not None:
                        if (isinstance(field, ForeignKey) or
                                isinstance(field, OneToOneField)):
                            related_model = get_model(
                                app_name, column.get_type_name())
                            value, created = \
                                related_model.objects.get_or_create(name=value)
                        elif isinstance(field, DateTimeField):
                            t = time.strptime(value, '%m/%d/%Y %H:%M:%S')
                            value = datetime.datetime(
                                t[0], t[1], t[2], t[3], t[4], t[5])
                        elif isinstance(field, DateField):
                            t = time.strptime(value, '%m/%d/%Y')
                            value = datetime.datetime(
                                t[0], t[1], t[2], t[3], t[4], t[5])

                        obj.__setattr__(field.name, value)

            obj.save()

            # set the many_to_many fields after the save
            # prior to the save, the object has no primary key,
            # so django is unable to do the lookup in the related many-to-many
            # table
            for field in opts.many_to_many:
                related_model_name = field.name.strip().replace('_', '')
                if related_model_name in columns.keys():
                    column = columns[related_model_name]
                    if column.value is not None:
                        related_model = get_model(
                            app_name, column.get_type_name())
                        for v in column.value.split(','):
                            related_obj, created = \
                                related_model.objects.get_or_create(name=v)
                            obj.__getattribute__(field.name).add(related_obj)

            obj.save()
        except:
            msg = "Unexpected error: %s-%s"
            print msg % (app_name, model._meta.verbose_name), sys.exc_info()

    def process_spreadsheets(self, model_spreadsheet_name, app_name):
        spreadsheet_feed = self.gd_client.GetSpreadsheetsFeed()
        for i, entry in enumerate(spreadsheet_feed.entry):
            if entry.title.text == model_spreadsheet_name:
                # parse out the sheet's identifying key
                # this is a bit of a hack, could use an XML parser to make this
                # nicer
                id_parts = entry.id.text.split('/')
                key = id_parts[len(id_parts) - 1]
                feed = self.gd_client.GetWorksheetsFeed(key)

                for i, entry in enumerate(feed.entry):
                    id_parts = entry.id.text.split('/')
                    worksheetId = id_parts[len(id_parts) - 1]
                    model = get_model(app_name, entry.title.text)

                    print "Processing data for %s" % model._meta.verbose_name

                    if model._meta.verbose_name == 'station':
                        msg = "Processing data for %s"
                        print msg % model._meta.verbose_name

                    feed = self.gd_client.GetListFeed(key, worksheetId)

                    for i, entry in enumerate(feed.entry):
                        self.process_model_object(entry, model, app_name)

                    # if model._meta.verbose_name == 'publication':
                    #  break

    def handle(self, *app_labels, **options):
        args = """Usage: python manage.py import --user user --pwd password
            --sheet model spreadsheet name --app django app name]"""

        if len(options) < 4:
            print args
            return
        elif not self.init_google_client(options.get('user'),
                                         options.get('pwd')):
            print args
            return
        else:
            print "Retrieving data for: ", self.gd_client.email

        # delete the old data, and make sure the roles are created
        self.prepare_database(options.get('app'))

        # process the spreadsheets
        self.process_spreadsheets(options.get('sheet'), options.get('app'))

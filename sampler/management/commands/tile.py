from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from optparse import make_option
from blackrock.sampler.models import *
import csv


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--csv', dest='csv', help='Base CSV file to tile'),
        make_option('--plotsize', dest='plotsize',
                    help='Original plot size. Assuming square dimensions'),
        make_option('--factor', dest='factor',
                    help='The factor by which to multiply the plot size'),
    )

    def handle(self, *app_labels, **options):
        args = 'Usage: python manage.py tile --csv csv file \
            --plotsize original size --factor multiplication factor]'

        if (not options.get('csv') or
            not options.get('plotsize') or
            not options.get('factor')):
            print args
            return

        plotsize = int(options.get('plotsize'))
        tiles = int(options.get('factor'))

        fh = open(options.get('csv'), 'r')
        table = csv.reader(fh)
        header = table.next()

        print '"ID","SPECIES","x","y","dbh"'

        for i in range(len(header)):
            h = header[i].lower()
            if h == 'id':
                id_idx = i
            if h == 'species':
                species_idx = i
            if h == 'x':
                x_idx = i
            if h == 'y':
                y_idx = i
            if h == 'dbh':
                dbh_idx = i

        trees = list(table)
        idmap = {}
        plot = 1

        y = 0
        while (y < tiles):
            x = 0
            while (x < tiles):
                # adjust each tree's position according to the plot we're in
                for tree in trees:
                    padded_id = "%04d" % int(tree[id_idx])
                    adjusted_id = int("%d%s" % (plot, padded_id))

                    # verify this adjusted_id is not going to be a duplicate
                    if (not idmap.has_key(adjusted_id)):
                        idmap[adjusted_id] = 1
                    else:
                        print "YOUR MOM ERROR: id overlap: %s. Contact your developer to fix the id adjustments" % adjusted_id
                        return

                    # figure out x/y offset, then add the tree's position
                    adjusted_x = x * plotsize + float(tree[x_idx])
                    adjusted_y = y * plotsize + float(tree[y_idx])
                    print '%s,%s,%s,%s,%s' % (adjusted_id, tree[species_idx], adjusted_x, adjusted_y, tree[dbh_idx])
                x += 1
                plot += 1  # increment factor tested to ensure that no ids overlap up to a factor of 10. note that making plot odd is pretty key to this.
            y += 1


from django.core.management.base import BaseCommand
from optparse import make_option
import csv
import sys

# Dataset preprocessing --
# Set missing oak species to O
# Set missing unknown species to U (optional)
# Calculate the global average dbh for each species set and use this
# number to populate missing dbh in the code

# Missing data instructions --
# * Missing DBH -- Fill in the blanks using a global average for a
#   given species set (oak, non-oak)
# * Missing Location - Drop the tree.
# * Missing Species -- Assumes it's a non-oak if the field is blank


class Command(BaseCommand):

    args = 'Usage: python manage.py oaktile --csv csv file'
    oaks = ["O", "RO", "WO", "CO", "BO", "SWO"]
    nonoaks = ["SM", "BG", "SH", "WA", "VP", "BB", "HH"]
    avg_oak_dbh = 43.9
    avg_nonoak_dbh = 20
    centered_data_plots = [
        "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
    plot_origin_xy = {"A1": [0, 0], "A2": [75, 0], "A3": [150, 0],
                      "A4": [225, 0], "B1": [0, 75], "B2": [75, 75],
                      "B3": [150, 75], "B4": [225, 75], "C1": [0, 150],
                      "C2": [75, 150], "C3": [150, 150], "C4": [225, 150]}

    idx = {}
    tree_id_counter = 1

    option_list = BaseCommand.option_list + (
        make_option('--csv', dest='csv',
                    help='Base CSV file containing oak and non-oak data. \
                    non-oak data will be tiled.'),
    )

    def get_value(self, lst, idx):
        try:
            value = lst[idx]
        except IndexError:
            value = ""
            pass
        return value

    def process_non_oak(self, plot, id, x, y, species, dbh):
        if (dbh == ""):
            dbh = self.avg_nonoak_dbh

        # for plots with a centered_data_plot, transform points to upper left
        # hand corner
        offsetx = x
        offsety = y
        if (plot in self.centered_data_plots):
            # subtract 25,25 from the x/y coordinates to transform the
            # coordinates to the upper left hand corner
            offsetx -= 25
            offsety -= 25

        origin_xy = self.plot_origin_xy[plot]
        if (offsetx < origin_xy[0] or
            offsetx > origin_xy[0] + 25 or
                offsety < origin_xy[1] or offsety > origin_xy[1] + 25):
            msg = "%s %s Tree Location (%s,%s) >> (%s, %s) is outside \
            the 25x25 plot. Removing tree from tiling\n"
            sys.stderr.write(msg % (plot, id, x, y, offsetx, offsety))
            return

        for tiles_y in range(3):
            for tiles_x in range(3):
                newx = offsetx + (25 * tiles_x)
                newy = offsety + (25 * tiles_y)
                print '%s,%s,%s,%s,%s' % (self.tree_id_counter, species,
                                          newx, newy, dbh)
                self.tree_id_counter += 1

    def handle(self, *app_labels, **options):
        if (not options.get('csv')):
            print self.args
            return

        fh = open(options.get('csv'), 'r')
        table = csv.reader(fh)
        header = table.next()
        for i in range(len(header)):
            self.idx[header[i].lower()] = i

        sys.stdout.write('"ID","SPECIES","x","y","dbh"\n')

        trees = list(table)
        for tree in trees:
            plot = self.get_value(tree, self.idx["plot"])
            id = self.get_value(tree, self.idx["id"])
            x = self.get_value(tree, self.idx["x"])
            y = self.get_value(tree, self.idx["y"])
            species = self.get_value(tree, self.idx["species"])
            dbh = self.get_value(tree, self.idx["dbh"])

            # If location is missing, skip the tree
            if x == "" or y == "":
                sys.stderr.write("%s %s Location Missing\n" % (plot, id))
                continue

            if (species in self.oaks):
                if (dbh == ""):
                    dbh = self.avg_nonoak_dbh

                print '%s,%s,%s,%s,%s' % (self.tree_id_counter,
                                          species, x, y, dbh)
                self.tree_id_counter += 1
            else:
                # If species is missing, assumes non-oak
                self.process_non_oak(
                    plot, id, float(x), float(y), species, dbh)

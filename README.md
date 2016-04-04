Black Rock
==========

The Virtual Forest Initiative supports and enhances research, education, and community activities at Black Rock Forest.  The forest, located 50 miles north of New York City in the Hudson Highlands, is a 4000-acre natural living laboratory for field-based scientific inquiry; it is operated by a unique consortium of colleges and universities, public and independent schools, and scientific and cultural institutions.


REQUIREMENTS
------------
Python 2.7  
Postgres  
SOLR 3.6

## SpatiaLite requirement ##
To run the tests, you need SpatiaLite installed for SQLite. Here's the
packages you need, depending on your OS:

Ubuntu 16.04:
- `libsqlite3-mod-spatialite`

Ubuntu 14.04:
- `libspatialite-dev`
- `python-spatialite2`

Homebrew (Mac OS X):
[Instructions here](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/install/spatialite/#homebrew)

If you get a "library not found" error when running `make test`, add
a line to `local_settings.py`, as documented [here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/#installing-spatialite):

    SPATIALITE_LIBRARY_PATH='mod_spatialite'

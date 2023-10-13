[![Actions Status](https://github.com/ccnmtl/blackrock/workflows/build-and-test/badge.svg)](https://github.com/ccnmtl/blackrock/actions)

Black Rock
==========

The Virtual Forest Initiative supports and enhances research, education, and community activities at Black Rock Forest.  The forest, located 50 miles north of New York City in the Hudson Highlands, is a 4000-acre natural living laboratory for field-based scientific inquiry; it is operated by a unique consortium of colleges and universities, public and independent schools, and scientific and cultural institutions.


REQUIREMENTS
------------
* Python 3.11
* PostgreSQL
* Apache Solr

## SpatiaLite requirement ##
To run the tests, you need SpatiaLite installed for SQLite. Here's the
packages you need, depending on your OS:

Debian/Ubuntu:
- `libsqlite3-mod-spatialite`

Homebrew (Mac OS X):
[Instructions here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/#homebrew)

If you get a "library not found" error when running `make test`, add
a line to `local_settings.py`, as documented [here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/#installing-spatialite):

    SPATIALITE_LIBRARY_PATH='mod_spatialite'

## PostGIS migration problem
If you get the error: `ERROR: must be owner of type spheroid` when running the migrations, try following these steps:
```
$ sudo -u postgres psql blackrock
blackrock=# drop table spatial_ref_sys;
blackrock=# drop table geometry_columns;
blackrock=# create extension postgis;
```
Then you should be able to run the migrations. I'm guessing this happens because of a version mis-match between the postgres/postgis used to export the database, and the versions in the local environment. This happened to me on Ubuntu 16.04.

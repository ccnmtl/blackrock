#!/bin/bash
# reimport the waterquality data
export PYTHONPATH="$PYTHONPATH:/var/www/blackrock/"
SETTINGS=$1
./manage.py import_harlem --settings=$SETTINGS
./manage.py import_harlem_rain --settings=$SETTINGS
./manage.py import_brf_stream --settings=$SETTINGS
./manage.py import_brf_lowlands --settings=$SETTINGS
./manage.py trim_data --settings=$SETTINGS
./manage.py avg_harlem --settings=$SETTINGS

#!/bin/bash
# reimport the waterquality data

./manage.py import_harlem
./manage.py import_harlem_rain
./manage.py import_brf_stream
./manage.py import_brf_lowlands
./manage.py trim_data
./manage.py avg_harlem

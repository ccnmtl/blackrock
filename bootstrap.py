#!/usr/bin/env python
import glob
import os
import sys
import subprocess
import shutil

pwd = os.path.abspath(os.path.dirname(__file__))
vedir = os.path.abspath(os.path.join(pwd, "ve"))

if os.path.exists(vedir):
    shutil.rmtree(vedir)

virtualenv_support_dir = os.path.abspath(
    os.path.join(pwd, "requirements", "virtualenv_support"))

ret = subprocess.call(["python", "virtualenv.py",
                       "--extra-search-dir=%s" % virtualenv_support_dir,
                       "--never-download",
                       vedir])
if ret:
    exit(ret)

ret = subprocess.call([os.path.join(vedir, 'bin', 'pip'), "install",
                       "-E", vedir,
                       "--index-url=''",
                       "--requirement",
                       os.path.join(pwd, "requirements/apps.txt")])
if ret:
    exit(ret)

if sys.version_info < (2, 7, 0):
    ret = subprocess.call(
        [os.path.join(vedir, 'bin', 'pip'), "install",
         "-E", vedir,
         os.path.join(pwd, "requirements/src/Imaging-1.1.7.tar.gz")])
else:
    ret = subprocess.call(
        [os.path.join(vedir, 'bin', 'pip'), "install",
         "-E", vedir,
         os.path.join(pwd, "requirements/src/Pillow-1.7.8.zip")])

if sys.version.startswith('2.6'):
    # have to do seperately or it breaks in 2.7
    ret = subprocess.call(
        [os.path.join(vedir, 'bin', 'pip'), "install",
         "-E", vedir,
         "--index-url=''",
         os.path.join(pwd, "requirements/src/importlib-1.0.1.tar.gz")])
    if ret:
        exit(ret)
    ret = subprocess.call(
        [os.path.join(vedir, 'bin', 'pip'), "install",
         "-E", vedir,
         "--index-url=''",
         os.path.join(pwd, "requirements/src/unittest2-0.5.1.tar.gz")])
    if ret:
        exit(ret)

subprocess.call([os.path.join(vedir, "bin/easy_install"),
                 os.path.join(pwd, "requirements/eggs/pytz-2011b-py2.6.egg")])

ret = subprocess.call(["python", "virtualenv.py", "--relocatable", vedir])
# --relocatable always complains about activate.csh, which we don't really
# care about. but it means we need to ignore its error messages

if ret:
    exit(ret)

# Copy a postgis adapter patch into the correct location
pattern = "%s/lib/python*/site-packages/django/contrib/gis/db/backends/postgis/adapter.py" % vedir
postgis_file = glob.glob(pattern)[0]
ret = subprocess.call(['cp', 'requirements/src/adapter.py', postgis_file])
if ret:
    exit(ret)

print "Postgres 9.1 postgis patch applied"

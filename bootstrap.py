#!/usr/bin/env python
import glob
import os
import shutil
import subprocess


pwd = os.path.abspath(os.path.dirname(__file__))
vedir = os.path.abspath(os.path.join(pwd, "ve"))

if os.path.exists(vedir):
    shutil.rmtree(vedir)

virtualenv_support_dir = os.path.abspath(
    os.path.join(
        pwd, "requirements", "virtualenv_support"))

ret = subprocess.call(["python", "virtualenv.py",
                       "--extra-search-dir=%s" % virtualenv_support_dir,
                       "--never-download",
                       vedir])
if ret:
    exit(ret)

ret = subprocess.call(
    [os.path.join(vedir, 'bin', 'pip'), "install",
     "--index-url=http://pypi.ccnmtl.columbia.edu/",
     "wheel==0.21.0"])

if ret:
    exit(ret)

ret = subprocess.call(
    [os.path.join(vedir, 'bin', 'pip'), "install",
     "--use-wheel",
     "--index-url=http://pypi.ccnmtl.columbia.edu/",
     "--requirement", os.path.join(pwd, "requirements.txt")])

if ret:
    exit(ret)

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

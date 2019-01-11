# flake8: noqa
from blackrock.settings_shared import *

try:
    from blackrock.local_settings import *
except ImportError:
    pass

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decouple import config


ENVIRONMENT = config('ENVIRONMENT')
SECRET_KEY = config('SECRET_KEY')

if ENVIRONMENT == 'local':
    from .local import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .production import *

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app
from decouple import config


ENVIRONMENT = config('ENVIRONMENT')
SECRET_KEY = config('SECRET_KEY')

if ENVIRONMENT == 'local':
    from .local import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .production import *


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
__all__ = ('celery_app',)

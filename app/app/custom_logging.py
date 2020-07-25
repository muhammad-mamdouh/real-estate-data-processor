# -*- coding: utf-8 -*-
from __future__ import unicode_literals


CUSTOM_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'console_default': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '[%d-%m-%Y %H:%M:%S]'
        },
        'console_detail': {
            'format': '\n%(asctime)s - %(levelname)-5s [%(name)s] [request_id=%(request_id)s] %(message)s',
            'datefmt': '[%d-%m-%Y %H:%M:%S]'
        },
        'detail': {
            'format': '\n%(asctime)s [request_id=%(request_id)s] %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['request_id'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_default'
        },
        'file': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'class': 'logging.FileHandler',
            'formatter': 'detail',
            'filename': 'logs/debug.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['request_id'],
            'formatter': 'detail',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'file_upload': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'detail',
            'class': 'logging.FileHandler',
            'filename': 'logs/file_upload.log',
        },
        'aggregate_specific_asset': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'detail',
            'class': 'logging.FileHandler',
            'filename': 'logs/aggregate_specific_asset.log',
        },
        'aggregate_all_assets': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'detail',
            'class': 'logging.FileHandler',
            'filename': 'logs/aggregate_all_assets.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'file_upload': {
            'handlers': ['file_upload'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'aggregate_specific_asset': {
            'handlers': ['aggregate_specific_asset'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'aggregate_all_assets': {
            'handlers': ['aggregate_all_assets'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

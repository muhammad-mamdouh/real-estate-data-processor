# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import os
import random
import string

from django.utils.translation import gettext_lazy as _


def get_client_ip(request):
    """
    Get client ip from the request object
    :param request: request object being made
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def logging_message(logger, head, request, message):
    """
    Simple function that will take the logger and the message and log them in an template format
    :param logger: the logger itself that will handle the log message
    :param head: the head/title of the log message
    :param request: the pure http request object
    :param message: the message that will be logged
    :return: The message will be logged into the specified logger
    """
    return logger.debug(_(f"{head}\nUser: {request.user} -- IP Address: {get_client_ip(request)}\n{message}"))


def update_filename(instance, filename):
    """
    update document name
    :param instance: doc instance
    :param filename: filename of uploaded file
    :return: file name updated
    """
    now = datetime.now()
    path = f"documents/{now.year}/{now.month}/{now.day}/"
    file, ext = filename.split('.')
    filename = file + '_' + '_' + \
               ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + \
               '.' + ext
    return os.path.join(path, filename)

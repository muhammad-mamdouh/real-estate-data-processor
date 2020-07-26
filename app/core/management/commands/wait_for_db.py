# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    help = "Django command to pause the execution until database is available"

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("\nWaiting for database...\n"))
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError :
                self.stdout.write(self.style.ERROR("\nDatabase unavailable, waiting 1 second...\n"))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("\nDatabase available!\n"))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractTimeStamp(models.Model):
    """
    Time stamp class for created_at and updated_at fields.
    """

    created_at = models.DateTimeField(
            _("Created At"),
            db_index=True,
            auto_now_add=True,
            null=True,
            blank=True
    )
    updated_at = models.DateTimeField(
            _("Updated At"),
            db_index=True,
            auto_now=True,
            null=True,
            blank=True
    )

    class Meta:
        abstract = True


class AbstractUnitType(models.Model):
    """
    Unit types classification
    """

    # Unit Types
    RESIDENTIAL = 'rs'
    COMMERCIAL = 'cm'
    OFFICE = 'of'
    RETAIL = 'rt'

    UNIT_TYPES_CHOICES = [
        (RESIDENTIAL, _("Residential")),
        (COMMERCIAL, _("Commercial")),
        (OFFICE, _("Office")),
        (RETAIL, _("Retail")),
    ]

    unit_type = models.CharField(
            _("Type"),
            max_length=2,
            choices=UNIT_TYPES_CHOICES,
            null=False,
            blank=False
    )

    class Meta:
        abstract = True

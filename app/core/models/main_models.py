# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import AbstractTimeStamp, AbstractUnitType


class Portfolio(AbstractTimeStamp):
    """
    Portfolio model is responsible for representing the different portfolio objects in the real estate industry.
    """

    name = models.CharField(
            _("Portfolio Name"),
            db_index=True,
            unique=True,
            max_length=254,
            null=False,
            blank=False
    )

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")
        get_latest_by = "-updated_at"
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        "String representation for the portfolio model objects"
        return self.name


class Asset(AbstractTimeStamp):
    """
    Asset model is responsible for representing the asset object in the real estate industry.
    """

    portfolio = models.ForeignKey(
            Portfolio,
            on_delete=models.CASCADE,
            related_name=_("assets"),
            verbose_name=_("Portfolio"),
            null=False,
            blank=False
    )
    reference = models.CharField(
            _("Asset Reference"),
            db_index=True,
            unique=True,
            max_length=254,
            null=False,
            blank=False
    )
    city = models.CharField(
            _("City"),
            max_length=254,
            null=False,
            blank=False
    )
    address = models.CharField(
            _("Address"),
            max_length=254,
            null=False,
            blank=False
    )
    zipcode = models.IntegerField(
            _("Zip Code"),
            null=False,
            blank=False
    )
    is_restricted = models.BooleanField(
            _("Is Restricted"),
            default=False,
            null=False,
            blank=False
    )
    year_of_construction = models.PositiveIntegerField(
            _("Year Of Construction"),
            validators=[
                MinValueValidator(1700),
                MaxValueValidator(datetime.now().year),
            ],
            help_text=("Use the following format: YYYY"),
            null=False,
            blank=False
    )

    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")
        get_latest_by = "-updated_at"
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        "String representation for the asset model objects"
        return self.reference


class Unit(AbstractTimeStamp, AbstractUnitType):
    """
    Unit model is responsible for representing the unit object in the real estate industry.
    """

    asset = models.ForeignKey(
            Asset,
            on_delete=models.CASCADE,
            related_name=_("units"),
            verbose_name=_("Asset"),
            null=False,
            blank=False
    )
    reference = models.CharField(
            _("Unit Reference"),
            db_index=True,
            unique=True,
            max_length=254,
            null=False,
            blank=False
    )
    is_rented = models.BooleanField(
            _("Is rented?"),
            default=False,
            null=False,
            blank=False
    )
    size = models.IntegerField(
            _("Size"),
            null=False,
            blank=False
    )
    rent = models.DecimalField(
            _("Rent"),
            max_digits=12,
            decimal_places=2,
            default='',
            null=True,
            blank=True
    )
    tenant = models.CharField(
            _("Tenant"),
            max_length=254,
            default='',
            null=True,
            blank=True
    )
    lease_start = models.DateField(
            _("Lease Start"),
            db_index=True,
            default='',
            null=True,
            blank=True
    )
    lease_end = models.DateField(
            _("Lease End"),
            db_index=True,
            default='',
            null=True,
            blank=True
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")
        get_latest_by = "-updated_at"
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        "String representation for the unit model objects"
        return self.reference

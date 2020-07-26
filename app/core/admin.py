# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Asset, Portfolio, Unit


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """
    Admin model for customizing the Portfolio admin view
    """

    list_display = ['name', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at', '-created_at']
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Important Dates'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """
    Admin model for customizing the Asset admin view
    """

    list_display = ['reference', 'portfolio', 'city', 'address', 'zipcode', 'is_restricted', 'year_of_construction']
    list_filter = ['portfolio__name', 'is_restricted', 'city']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at', '-created_at']
    fieldsets = (
        (None, {
            'fields': list_display
        }),
        (_('Important Dates'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """
    Admin model for customizing the Unit admin view
    """

    list_display = ['reference', 'asset', 'unit_type', 'size', 'is_rented', 'tenant', 'rent', 'lease_end']
    list_filter = ['asset__reference', 'unit_type', 'is_rented']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at', '-created_at']
    fieldsets = (
        (None, {
            'fields': ('asset', 'reference', 'unit_type', 'size', 'is_rented', 'tenant', 'rent')
        }),
        (_('Important Dates'), {
            'fields': ('lease_start', 'lease_end', 'created_at', 'updated_at')
        }),
    )

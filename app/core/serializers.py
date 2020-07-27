# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from rest_framework import serializers

from .models import Asset


class AssetInfoAggregationReadSerializer(serializers.Serializer):
    """
    Serializes asset info aggregation request
    """

    asset_ref = serializers.CharField(max_length=254, required=False, allow_null=True, allow_blank=True)


class AssetInfoAggregationWriteSerializer(serializers.ModelSerializer):
    """
    Serializes asset info aggregation response
    """

    restricted_area = serializers.SerializerMethodField()
    number_of_units = serializers.SerializerMethodField()
    total_rent = serializers.SerializerMethodField()
    total_area = serializers.SerializerMethodField()
    area_rented = serializers.SerializerMethodField()
    vacancy = serializers.SerializerMethodField()
    walt = serializers.SerializerMethodField()
    latest_update = serializers.SerializerMethodField()

    def get_restricted_area(self, asset_object):
        """Retrieves asset restriction status"""
        return asset_object.is_restricted

    def get_number_of_units(self, asset_object):
        """Retrieves asset's total number of units"""
        return asset_object.units.count()

    def get_total_rent(self, asset_object):
        """Retrieves asset's total amount of rent for the rented units"""
        return sum([unit.rent for unit in asset_object.units.all() if unit.is_rented])

    def get_total_area(self, asset_object):
        """Retrieves asset's total units sizes"""
        return sum([unit.size for unit in asset_object.units.all()])

    def get_area_rented(self, asset_object):
        """Retrieves asset's total rented units sizes"""
        return sum([unit.size for unit in asset_object.units.all() if unit.is_rented])

    def get_vacancy(self, asset_object):
        """
        Retrieves asset's vacancy rate
        How it is being calculated:
            1. Multiply the number of vacant units by 100.
            2. Divide the result by the total number of units in the property.
        """
        if asset_object.units.count() > 0:
            vacancy = (asset_object.units.filter(is_rented=False).count() * 100) / asset_object.units.count()
            return f"{round(vacancy, 2)} %"

        return "0.0 %"

    def get_walt(self, asset_object):
        """
        The WALT is an important measurement for owners of commercial properties to estimate the vacancy risks.
        It's a great KPI (key performance indicator) to let the owner know when properties are likely to fall vacant.
        How it is being calculated:
            * Calculate the tenanted area per property and multiply by the years of the occupancy
        """
        all_tenanted_units = asset_object.units.filter(is_rented=True)
        walt = 0.0

        if all_tenanted_units.count() > 0:
            total_rentable_area = sum([unit.size for unit in asset_object.units.all()])
            tenants_values_list = []
            for unit in all_tenanted_units:
                remaining_years = unit.lease_end.year - timezone.now().year
                tenant_occupation_ratio = unit.size/total_rentable_area
                tenants_values_list.append((round((tenant_occupation_ratio * remaining_years), 3)))

            walt = sum(tenants_values_list)

        return f"{round(walt, 1)} years"

    def get_latest_update(self, asset_object):
        """Retrieves asset's last update date"""
        if asset_object.units.count() > 0:
            return asset_object.units.all().first().updated_at.strftime("%d.%m.%Y")

        return asset_object.updated_at.strftime("%d.%m.%Y")

    class Meta:
        model = Asset
        fields = [
            "address", "zipcode", "city", "year_of_construction", "restricted_area", "number_of_units", "total_rent",
            "total_area", "area_rented", "vacancy", "walt", "latest_update"
        ]

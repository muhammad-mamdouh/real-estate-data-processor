# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import logging
import pandas as pd

from django.utils import timezone
from django.utils.translation import gettext as _

from rest_framework import serializers

from .models import Asset, Document
from .utils import logging_message


UNICODE = set(';:></*%$.\\')
TASK_UPLOAD_FILE_MAX_SIZE = 5242880
MIME_UPLOAD_FILE_TYPES = ['plain', 'octet-stream']
TASK_UPLOAD_FILE_TYPES = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'text/csv',
    'csv',
    'vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'vnd.openxmlformats-officedocument.wordprocessingml.document',
    'vnd.ms-excel',
]


FILE_UPLOAD_LOGGER = logging.getLogger("file_upload")


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
                lease_end_date = unit.lease_end.year if unit.lease_end else timezone.now().year
                remaining_years = lease_end_date - timezone.now().year
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


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes document files
    """

    class Meta:
        model = Document
        fields = ['file']

    def _validate_file_type(self, file):
        """
        :param file: uploaded file object
        :return: tuple of file type/extension and error if any
        """
        error = False
        file_type = file.content_type.split('/')[1]
        number_of_dots = len(file.name.split('.'))
        is_valid_sheet_extension = file.name.endswith(('.csv', '.xls', '.xlsx'))

        if not is_valid_sheet_extension or file_type not in TASK_UPLOAD_FILE_TYPES or number_of_dots != 2:
            error = "File type is not supported"

        return file_type, error

    def _validate_file_name(self, file):
        """
        :param file: uploaded file object
        :return: tuple of file name without the extension and errors if any
        """
        filename = error = False

        try:
            filename = "".join(file.name.split('.')[:-1])

            if any((char in UNICODE) for char in filename):
                error = "Filename should not include any unicode characters ex: >, <, /, $, * "
        except ValueError:
            error = "File name is not proper"

        return filename, error

    def _validate_file_size(self, file):
        """
        :param file: uploaded file object
        :return: tuple of file size and errors if any
        """
        error = "Please keep the file size under 5 MB" if file.size > TASK_UPLOAD_FILE_MAX_SIZE else False

        return file.size, error

    def _determine_csv_delimiter(self, file):
        """
        :param file: uploaded file object
        :return: the delimiter used at the csv sheet or False if there is any problem
        """

        try:
            as_string = file.read().decode("utf-8")
            dialect = csv.Sniffer().sniff(as_string)
            return dialect.delimiter
        except:
            return False

    def _validate_file_headers(self, file):
        """
        :param file: uploaded file object
        :return: tuple of valid file headers and errors if any
        """
        valid_headers = [
            "portfolio", "asset_ref", "asset_address", "asset_zipcode", "asset_city", "asset_is_restricted",
            "asset_yoc", "unit_ref", "unit_size", "unit_is_rented", "unit_rent", "unit_type", "unit_tenant",
            "unit_lease_start", "unit_lease_end", "data_timestamp"
        ]
        HEADERS_ERROR_MSG = f"Sheet headers are not proper, the valid headers naming and order is {valid_headers}"

        try:
            if file.name.endswith(".csv"):
                delimiter = self._determine_csv_delimiter(file)
                file.seek(0)
                df = pd.read_csv(file, sep=delimiter)
            else:
                df = pd.read_excel(file)

            error = False if df.columns.tolist() == valid_headers else HEADERS_ERROR_MSG
        except:
            error = "File data is not proper, check it and upload it again."

        return valid_headers, error

    def validate(self, attrs):
        """
        :param attrs: serializer attributes, currently the file object
        :return: adds custom validations for the file object
        """
        file = attrs.get('file', None)

        file_type, file_type_error = self._validate_file_type(file)
        file_name, file_name_error = self._validate_file_name(file)
        file_size, file_size_error = self._validate_file_size(file)
        file_headers, file_headers_error = self._validate_file_headers(file)

        if any([file_type_error, file_name_error, file_size_error, file_headers_error]):
            if file_type_error:
                error = file_type_error
            elif file_name_error:
                error = file_name_error
            elif file_size_error:
                error = file_size_error
            else:
                error = file_headers_error

            message = f"File name: {file_name} - file type: {file_type} - file size: {file.size}\nError: {error}"
            logging_message(FILE_UPLOAD_LOGGER, "[UPLOAD VALIDATION ERROR]", self.context["request"], message)
            raise serializers.ValidationError(_(error))

        return attrs

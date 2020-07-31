# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Portfolio, Asset, Unit


ASSETS_INFO_AGGREGATION_API_URL = reverse("core:aggregate_assets")
UPLOAD_FILE_API_URL = reverse("core:upload_file-list")


class PublicCoreAPIsTests(TestCase):
    """
    Tests for the core app api endpoints
    """

    def create_new_portfolio(self):
        """Create new portfolio"""
        self.portfolio_name = "Test Portfolio"
        self.portfolio_obj = Portfolio.objects.create(name=self.portfolio_name)

    def create_new_assets(self):
        """Create two assets"""
        self.asset_1_reference = "A_1"
        self.asset_2_reference = "A_2"
        self.city = "Berlin"
        self.address_1 = "Am Kupfergraben 1"
        self.address_2 = "Am Kupfergraben 2"
        self.zipcode = 10117
        self.zipcode = 10117
        self.is_restricted = True
        self.year_of_construction = 2000
        self.asset_obj_1 = Asset.objects.create(
                portfolio=self.portfolio_obj, reference=self.asset_1_reference, city=self.city, address=self.address_1,
                zipcode=self.zipcode, is_restricted=self.is_restricted, year_of_construction=self.year_of_construction
        )
        self.asset_obj_2 = Asset.objects.create(
                portfolio=self.portfolio_obj, reference=self.asset_2_reference, city=self.city, address=self.address_2,
                zipcode=self.zipcode, is_restricted=self.is_restricted, year_of_construction=self.year_of_construction
        )

    def create_new_units(self):
        """Create two units"""
        self.unit_1_reference = "A_1_1"
        self.unit_2_reference = "A_2_1"
        self.is_rented = True
        self.size = 900
        self.rent = Decimal(5000)
        self.tenant = "Mohamed Mamdouh"
        self.lease_start = "2020-08-01"
        self.unit_obj_1 = Unit.objects.create(
                asset=self.asset_obj_1, reference=self.unit_1_reference, is_rented=self.is_rented, size=self.size,
                rent=self.rent, tenant=self.tenant, lease_start=self.lease_start
        )
        self.unit_obj_2 = Unit.objects.create(
                asset=self.asset_obj_2, reference=self.unit_2_reference, is_rented=self.is_rented, size=self.size,
                rent=self.rent, tenant=self.tenant, lease_start=self.lease_start
        )

    def setUp(self):
        self.create_new_portfolio()
        self.create_new_assets()
        self.create_new_units()
        self.client = APIClient()

    def test_retrieving_all_assets_aggregated_info(self):
        """Test retrieving all assets aggregated info API endpoint"""
        response = self.client.get(ASSETS_INFO_AGGREGATION_API_URL)
        all_assets = Asset.objects.all().order_by("-updated_at")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], all_assets.count())

    def test_retrieving_specific_asset_aggregated_info(self):
        """Test retrieving specific asset aggregated info API endpoint"""
        asset_obj = Asset.objects.get(reference="A_2")
        response = self.client.get(ASSETS_INFO_AGGREGATION_API_URL, {"asset_ref": asset_obj.reference})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["address"], asset_obj.address)

    def test_uploading_portfolio_data_sheet_via_api(self):
        """Test uploading portfolio data in a sheet using upload API endpoint"""
        with open("media/portfolio_data_sheet.csv") as fp:
            response = self.client.post(UPLOAD_FILE_API_URL, {"file": fp})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(response.data["File Uploaded"])
            self.assertTrue(response.data["Status"])

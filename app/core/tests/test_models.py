# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import Portfolio, Asset, Unit, Document


class ModelTests(TestCase):
    """
    Tests for the core app models
    """

    def create_new_portfolio(self):
        """Create new portfolio"""
        self.portfolio_name = "Test Portfolio"
        self.portfolio_obj = Portfolio.objects.create(name=self.portfolio_name)

    def create_new_asset(self):
        """Create new asset"""
        self.asset_reference = "A_1"
        self.city = "Berlin"
        self.address = "Am Kupfergraben 6"
        self.zipcode = 10117
        self.is_restricted = True
        self.year_of_construction = 2000
        self.asset_obj = Asset.objects.create(
                portfolio=self.portfolio_obj, reference=self.asset_reference, city=self.city, address=self.address,
                zipcode=self.zipcode, is_restricted=self.is_restricted, year_of_construction=self.year_of_construction
        )

    def create_new_unit(self):
        """Create new unit"""
        self.unit_reference = "A_1_1"
        self.is_rented = True
        self.size = 900
        self.rent = Decimal(5000)
        self.tenant = "Mohamed Mamdouh"
        self.lease_start = "2020-08-01"
        self.unit_obj = Unit.objects.create(
                asset=self.asset_obj, reference=self.unit_reference, is_rented=self.is_rented, size=self.size,
                rent=self.rent, tenant=self.tenant, lease_start=self.lease_start
        )

    def setUp(self):
        self.create_new_portfolio()
        self.create_new_asset()
        self.create_new_unit()

    def test_successful_creating_portfolio(self):
        """Test successfully creating new portfolio"""

        self.assertEqual(self.portfolio_obj.name, self.portfolio_name)
        self.assertEqual(str(self.portfolio_obj), self.portfolio_name)

    def test_successful_creating_asset(self):
        """Test successfully creating new asset"""

        self.assertEqual(self.asset_obj.reference, self.asset_reference)
        self.assertEqual(str(self.asset_obj), self.asset_reference)

    def test_successful_creating_unit(self):
        """Test successfully creating new unit"""

        self.assertEqual(self.unit_obj.reference, self.unit_reference)
        self.assertEqual(str(self.unit_obj), self.unit_reference)

    def test_successful_creating_document(self):
        """Test successfully creating new document"""
        test_file = SimpleUploadedFile("portfolio_data.csv", b"file_content")
        document_obj = Document.objects.create(file=test_file)

        self.assertTrue(document_obj.file)

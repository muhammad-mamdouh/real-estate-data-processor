# -*- coding: utf-8 -*-
from django.urls import path

from .views import AssetInfoAggregationAPIView


app_name = 'core'

urlpatterns = [
    path('assets/', AssetInfoAggregationAPIView.as_view(), name='aggregate_assets'),
]

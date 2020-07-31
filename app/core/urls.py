# -*- coding: utf-8 -*-
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AssetInfoAggregationAPIView, UploadDocumentViewSet


app_name = 'core'
router = DefaultRouter()
router.register('', UploadDocumentViewSet, basename='upload_file')

urlpatterns = [
    path('upload/', include(router.urls)),
    path('assets/', AssetInfoAggregationAPIView.as_view(), name="aggregate_assets"),
]

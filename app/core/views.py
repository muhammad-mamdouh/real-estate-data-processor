# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext as _

from .mixins import APIViewPaginatorMixin
from .models import Asset, Document
from .serializers import AssetInfoAggregationReadSerializer, AssetInfoAggregationWriteSerializer, DocumentSerializer
from .utils import logging_message

ASSETS_INFO_AGGREGATION_LOGGER = logging.getLogger("assets_info_aggregation")

EXTERNAL_ERROR_MSG = _("Process stopped during an internal error, please try again or contact your support team")


class AssetInfoAggregationAPIView(APIViewPaginatorMixin, APIView):
    """
    Retrieves one/list of aggregated info about existed assets.
    """

    read_serializer = AssetInfoAggregationReadSerializer
    write_serializer = AssetInfoAggregationWriteSerializer

    def list(self, request, *args, **kwargs):
        """Serializes response of asset(s) aggregated info"""
        asset_ref = self.kwargs["ref"]

        if asset_ref:
            queryset = Asset.objects.filter(reference=asset_ref)
            if queryset.count() == 0:
                return Response({
                    "Error": _(f"No asset found with reference {asset_ref}")
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Asset.objects.all()

        if queryset.count() > 0:
            queryset = queryset.prefetch_related("units")
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.write_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.write_serializer(queryset, many=True)
            return Response(serializer.data)

        return Response({"Error": _("No Assets found at the system")}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        """Handles GET requests to retrieve one/list of aggregated info about existed assets."""

        serializer = self.read_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.kwargs["ref"] = serializer.validated_data["asset_ref"] if len(serializer.validated_data) > 0 \
                else False
            logging_message(ASSETS_INFO_AGGREGATION_LOGGER, "[REQUEST PAYLOAD]", request, serializer.validated_data)
            return self.list(request, *args, **kwargs)

        except ValidationError as err:
            logging_message(ASSETS_INFO_AGGREGATION_LOGGER, "[VALIDATION ERROR]", request, serializer.errors)
            return Response({"Validation Error": _(f"{err.args[0]}")}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            logging_message(ASSETS_INFO_AGGREGATION_LOGGER, "[INTERNAL ERROR]", request, err.args)
            return Response({"Internal Error": EXTERNAL_ERROR_MSG}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadDocumentViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling the uploaded portfolio data sheets
    """

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView

from experimenter.experiments.api.v6.serializers import (
    NimbusExperimentSerializer,
)
from experimenter.experiments.models import NimbusExperiment
from experimenter.features.manifests.nimbus_fml_loader import NimbusFmlLoader


class NimbusExperimentViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "slug"
    queryset = (
        NimbusExperiment.objects.with_related()
        .exclude(status__in=[NimbusExperiment.Status.DRAFT])
        .order_by("slug")
    )
    serializer_class = NimbusExperimentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_first_run"]


class NimbusExperimentDraftViewSet(NimbusExperimentViewSet):
    queryset = (
        NimbusExperiment.objects.with_related()
        .filter(status=NimbusExperiment.Status.DRAFT)
        .order_by("slug")
    )
    filterset_fields = ["is_localized"]


class NimbusExperimentFirstRunViewSet(NimbusExperimentViewSet):
    queryset = (
        NimbusExperiment.objects.with_related()
        .filter(status=NimbusExperiment.Status.LIVE)
        .filter(is_first_run=True)
        .order_by("slug")
    )


class NimbusFmlDiagnosticsApiSchema(AutoSchema):  # pragma: no cover
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        operation["parameters"] = [
            {
                "name": "application",
                "in": "query",
                "required": True,
                "schema": {"type": "string"},
            },
            {
                "name": "channel",
                "in": "query",
                "required": True,
                "schema": {"type": "string"},
            },
            {
                "name": "blob",
                "in": "query",
                "required": True,
                "schema": {"type": "string"},
            },
        ]
        return operation


class NimbusFmlDiagnosticsApi(APIView):
    def post(self, request):  # pragma: no cover
        self.schema = NimbusFmlDiagnosticsApiSchema
        application = request.POST.get("application")
        channel = request.POST.get("channel")
        blob = request.POST.get("blob")

        loader = NimbusFmlLoader(application, channel)
        fml_errors = loader.get_fml_errors(blob)
        
        return Response(fml_errors, status=status.HTTP_201_CREATED)

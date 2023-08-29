from django.urls import re_path

from experimenter.health.views import NimbusFeatureHealthView

urlpatterns = [
    re_path(
        r"^health", NimbusFeatureHealthView.as_view(), name="health"
    ),
]

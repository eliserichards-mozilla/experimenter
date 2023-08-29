from django.views.generic import DetailView
from django.views.generic import View
from django.views.generic import TemplateView

from experimenter.experiments.models import NimbusFeatureConfig

class NimbusFeatureHealthView(TemplateView):
    model = NimbusFeatureConfig
    context_object_name = "feature_configs"
    template_name = "health/dashboard.html"

    def get_queryset(self):
        return NimbusFeatureConfig.objects.all()
from django.test import TestCase

from experimenter.experiments.api.v5.serializers import (
    NimbusFmlErrorDataClass,
    NimbusFmlErrorSerializer,
)

class TestNimbusFmlErrorSerializer(TestCase):
    def test_valid_serializer(self):
        serializer = NimbusFmlErrorSerializer(NimbusFmlErrorDataClass())
        self.assertTrue(serializer.is_valid())
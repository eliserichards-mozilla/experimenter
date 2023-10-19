from django.test import TestCase

from experimenter.experiments.api.v5.serializers import (
    NimbusFmlErrorDataClass,
    NimbusFmlErrorSerializer,
)


class TestNimbusFmlErrorSerializer(TestCase):
    def test_valid_serializer(self):
        fml_error = NimbusFmlErrorDataClass(
            line=0,
            col=0,
            message="Incorrect value",
            highlight="enabled",
        )

        serializer = NimbusFmlErrorSerializer(fml_error)
        self.assertEqual(serializer.data["line"], fml_error.line)
        self.assertEqual(serializer.data["col"], fml_error.col)
        self.assertEqual(serializer.data["message"], fml_error.message)
        self.assertEqual(serializer.data["highlight"], fml_error.highlight)

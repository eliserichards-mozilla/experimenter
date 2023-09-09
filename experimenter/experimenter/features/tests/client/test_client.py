import json

from django.core.checks import Error
from django.test import TestCase
from experimenter.features.client.fml_client import FmlClient

from experimenter.features import (
    Features,
)
from experimenter.features.tests import (
    mock_valid_features,
)


@mock_valid_features
class TestClient(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Features.clear_cache()

    def test_filter_features(self):
        client = FmlClient()
        
        features = {
            "feature1": [112, 113],
            "feature2": [112],
            "feature3": [111],
            "feature4": [111, 112, 113],
        }

        versions = [112, 113]
        list_of_features_with_versions = client.fetch_features_for_versions(features, versions)
        self.assertEqual(len(list_of_features_with_versions), 3)
        self.assertEqual(
            list_of_features_with_versions,
            {"feature1": [112, 113], "feature2": [112], "feature4": [112, 113], }
        )


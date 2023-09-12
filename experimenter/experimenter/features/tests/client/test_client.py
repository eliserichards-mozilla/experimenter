import json

from django.core.checks import Error
from django.test import TestCase
from experimenter.features.client.fml_client import NimbusFmlClient
from unittest.mock import MagicMock, patch

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

    @patch("nimbus-experimenter.fml")
    def test_intiate_new_fml_client_no_error(self):
        application = "fenix"
        channel = "production"

        mock_fml = MagicMock()
        mock_fml_client.application = 
        mock_fml_client.json.return_value = {"data": []}
        client = NimbusFmlClient(application, channel)

        self.assertEqual(client.application, application)
        self.assertEqual(client.channel, channel)
        self.assertEqual(client.fml_client, "")
        
    def test_intiate_invalid_fml_client_errors(self):
        application = "rats"
        channel = "production"
        with patch("FmlClient.new") as mock_fml_new:
            try {
                client = NimbusFmlClient(application, channel)
            } catch (e: Error) {
                self.assertEqual(e, "Failed to find fml path: ../configs/rats.yaml")
            }
        self.assertEqual(len(mock_fml_new.mock_calls), 1)


    def test_filter_features(self):
        client = NimbusFmlClient(application="fenix", channel="production")
        
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

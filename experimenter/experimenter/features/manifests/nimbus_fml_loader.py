import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from rust_fml import FmlClient, FmlFeatureInspector

from experimenter.experiments.constants import NimbusConstants
from experimenter.experiments.models import NimbusFeatureVersion
from experimenter.settings import BASE_DIR

logger = logging.getLogger()


class NimbusFmlLoader:
    MANIFEST_PATH = Path(BASE_DIR, "features", "manifests")

    def __init__(self, application: str):
        self.application: str = (
            application if application in NimbusConstants.Application else None
        )

    @classmethod
    @lru_cache
    def create_loader(cls, application: str):
        return cls(application)

    def file_path(self, channel: str, version: Optional[NimbusFeatureVersion]):
        """Get path to release feature manifest from experimenter (local)."""
        if self.application is not None:
            path = Path(self.MANIFEST_PATH, self.application)
            if version:
                path /= str(version)
            path /= f"{channel}.fml.yaml"
            if Path.exists(path):
                return path
        else:
            logger.error(
                "Nimbus FML Loader: Invalid application. Failed to get local "
                "feature manifest."
            )
        return None

    # # Todo: Add versioning https://mozilla-hub.atlassian.net/browse/EXP-3875
    # def _get_fml_clients(self) -> list[FmlClient]:
    #     clients = []
    #     if file_path := self.file_path():
    #         client = self.fml_client(str(file_path), self.channel)
    #         if client is not None:
    #             clients.append(client)
    #         else:
    #             logger.error(
    #                 "Nimbus FML Loader: "
    #                 f"Failed to create FML clients for file path {file_path} and "
    #                 f"channel {self.channel}."
    #             )
    #     return clients

    @lru_cache  # noqa: B019
    def fml_client(self, channel: str, version: Optional[NimbusFeatureVersion]) -> FmlClient:
        channel: str = channel if channel in NimbusConstants.Channel else None
        return FmlClient(
            self.file_path(channel, version),
            channel,
        )

    def _get_inspectors(
        self, clients: list[FmlClient], feature_id: str
    ) -> list[FmlFeatureInspector]:
        return [
            inspector
            for inspector in (
                client.get_feature_inspector(feature_id) for client in clients
            )
            if inspector is not None
        ]

    @staticmethod
    def _get_errors(inspector: FmlFeatureInspector, blob: str):
        return inspector.get_errors(blob)

    # Todo: Add versioning https://mozilla-hub.atlassian.net/browse/EXP-3875
    def get_fml_errors(
        self, 
        blob: str, 
        feature_id: str,
        channel: str,
        version: Optional[NimbusFeatureVersion],
    ):
        """Fetch errors from the FML. This method creates FML clients, which are
        used by `FmlFeatureInspector`s to fetch errors based on the blob of text and
        the given feature.

        Returns:
            A list of feature manifest errors.
        """
        if self.application is not None:
            errors = []
            client = self.fml_client(channel, version)
            inspector = client.get_feature_inspector(feature_id)
            if inspector:
                errs = inspector.get_errors(blob)
                if errs := self._get_errors(inspector, blob):
                    errors.extend(errs)
            return errors
        else:
            logger.error(
                "Nimbus FML Loader: Invalid application. Failed to fetch FML errors."
            )
            return []

import logging
import os
import yaml

from nimbus-experimenter import FmlClient

logger = logging.getLogger()

class FeatureDescriptor:
  def id(): str
  def description(): str
#   def hash(): usize 

class NimbusFmlClient():    
    def __init__(self, application: str, channel: str, versions: list[str]): 
        self.application: str = application
        self.channel: str = channel
        self.versions: list[str] = versions
        
        fml_local = ""
        path :str = os.path.join("../configs", f"{application}.yaml")

        if os.path.exists(path):
            with open(path) as application_yaml_file:
                application_data = yaml.load(
                    application_yaml_file.read(), Loader=yaml.Loader
                )
                for feature_slug in application_data:
                    if(application_data[feature_slug]) is application:
                        fml_local = application_data["repo"] + application_data["fml_path"]
        if fml_local != "":
            self.fml_client = FmlClient.new(path, channel)
            logger.info("FML client created")
            # features: list[str] = self.fml_client.get_feature_ids()
            # for id in features:
            #     descriptor: FeatureDescriptor = self.fml_client.get_feature_descriptor(id)
            
            # features: list[FeatureDescriptor] = fm.get_features()
        else: 
            logger.error("Failed to find fml path: " + path)
    
    def get_features(self, versions):
        if self.fml_client == "":
            logger.error("No FML client, can\'t fetch manifests")
            return {}
        else:
            ids = {}
            for v in versions:
                manifests = self.get_manifests(v)
                for m in manifests:
                    ids.update({v: m.get_feature_ids()})
            return ids
    
    def get_feature_description(self, feature_id):
        return self.get_feature_descriptor(feature_id)

    def get_manifests(self, versions):
        manifests = []
        for v in versions:
            manifests.append(self.get_manifest(v))
        return manifests

    def fetch_features_for_versions(self, versions):
        features = self.get_feature_ids(versions)
        list_of_features_with_any_versions = {}
        for f in features:
            versions_set = set(features[f]).intersection(set(versions))
            if versions_set:
                list_of_features_with_any_versions[f] = sorted(list(versions_set))
        return list_of_features_with_any_versions

    def fetch_features_for_versions(self, versions):
        features = self.get_feature_ids(versions)
        list_of_features_with_any_versions = {}
        for f in features:
            versions_set = set(features[f]).intersection(set(versions))
            if versions_set:
                list_of_features_with_any_versions[f] = sorted(list(versions_set))
        return list_of_features_with_any_versions

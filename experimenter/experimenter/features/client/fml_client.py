import logging

logger = logging.getLogger()

class FmlClient():
    def create(): 
        # todo: create FML client, https://mozilla-hub.atlassian.net/browse/EXP-3791
        logger.info("FML client created")
    
    def get_feature_ids(self, versions):
        ids = []
        for v in versions:
            ids.append(self.get_feature_ids())
        return ids

    def fetch_features_for_versions(self, features, versions):
        list_of_features_with_any_versions = {}
        for f in features:
            versions_set = set(features[f]).intersection(set(versions))
            if versions_set:
                list_of_features_with_any_versions[f] = sorted(list(versions_set))
        return list_of_features_with_any_versions

# {
#   feature1: [112, 113]
#   feature2: [112]
#   feature3: [111]
#   feature4: [111, 112, 113]
# }

# {
#   111: [feature3, feature4]
#   112: [feature1, feature3, feature4]
# }

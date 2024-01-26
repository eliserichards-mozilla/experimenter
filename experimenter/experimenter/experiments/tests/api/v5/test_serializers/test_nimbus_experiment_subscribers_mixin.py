from django.contrib.auth.models import User
from django.test import TestCase

from experimenter.experiments.api.v5.serializers import NimbusExperimentSerializer
from experimenter.experiments.models import NimbusExperiment
from experimenter.experiments.tests.factories import NimbusExperimentFactory
from experimenter.openidc.tests.factories import UserFactory


class TestNimbusExperimentSubscribersMixin(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()

    def test_can_update_subscribers(self):
        subscriber: User = UserFactory.create()
        experiment = NimbusExperimentFactory.create_with_lifecycle(
            NimbusExperimentFactory.Lifecycles.LIVE_APPROVE_APPROVE,
            application=NimbusExperiment.Application.DESKTOP,
            subscribers=[],
        )

        serializer = NimbusExperimentSerializer(
            experiment,
            {
                "subscribers": [subscriber.id],
                "changelog_message": "Test unsubscribe",
            },
            context={"user": subscriber},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        experiment = serializer.save()
        self.assertEqual(list(experiment.subscribers.all()), [subscriber])

    def test_can_remove_subscribers(self):
        subscriber = UserFactory.create()
        experiment = NimbusExperimentFactory.create_with_lifecycle(
            NimbusExperimentFactory.Lifecycles.LIVE_APPROVE_APPROVE,
            application=NimbusExperiment.Application.DESKTOP,
            subscribers=[subscriber],
        )

        serializer = NimbusExperimentSerializer(
            experiment,
            {
                "subscribers": [],
                "changelog_message": "Test unsubscribe",
            },
            context={"user": subscriber},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        experiment = serializer.save()
        self.assertEqual(list(experiment.subscribers.all()), [])

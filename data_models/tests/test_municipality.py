from django.test import TestCase

from data_models.models import Municipality


class MunicipalityTest(TestCase):
    def test_load_municipalities(self):
        # Checks that the data migrations worked
        self.assertEqual(len(Municipality.objects.all()), 99)
